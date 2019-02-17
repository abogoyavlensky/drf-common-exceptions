# -*- coding: utf-8 -*-
"""
    drf-common-exception/exceptions.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implementation of common exception handler for Django REST framework.

    :copyright: (c) 2019 by Andrey Bogoyavlensky.
"""
from __future__ import absolute_import, unicode_literals

import collections
import sys
from builtins import str as text
from collections import OrderedDict

from rest_framework import exceptions, status
from rest_framework.serializers import Serializer
from rest_framework.settings import api_settings
from rest_framework.views import exception_handler as origin_exception_handler

# TODO: make configurable from settings
NON_FIELD_ERRORS_KEY_LABEL = None


def get_service(view):
    """Returns service name by view and stacktrace."""
    service = ".".join([view.__class__.__module__, view.__class__.__name__])
    _, _, tb = sys.exc_info()
    tb = getattr(tb, "tb_next", tb)
    return ":".join([service, text(tb.tb_lineno)])


def get_label(path, serializer):
    """Return label for field by serializer data."""
    if not serializer:
        return NON_FIELD_ERRORS_KEY_LABEL
    field_name, tail = path[0], path[1:]
    if field_name == api_settings.NON_FIELD_ERRORS_KEY:
        return NON_FIELD_ERRORS_KEY_LABEL
    field = serializer.fields.get(field_name)
    if isinstance(field, Serializer) and tail:
        return get_label(tail, field)
    return getattr(field, "label", "")


def flatten_dict(d, parent_key="", sep="."):
    """Return nested dict as single level dict."""
    items = []
    for k, v in d.items():
        new_key = sep.join([parent_key, k]) if parent_key and sep else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def handle_errors(value):
    """Return list error messages from value."""
    errors = value if isinstance(value, list) else [value]
    return [text(e) for e in errors]


def common_exception_handler(exc, context):
    """Add single format for exception and validation errors.
    Example error:
        {
            "service": "apps.users.viewsets.UserViewSet:20",
            "error": "ValidationError",
            "detail": [
                {
                    "label": "Name",
                    "field": "name",
                    "messages": [
                        "This is required field."
                    ]
                }
            ]
        }
    """
    response = origin_exception_handler(exc, context)
    if response is not None:
        # Detail
        if isinstance(response.data, dict) and "detail" in response.data:
            detail = response.data.get("detail")
        else:
            detail = response.data
        if isinstance(detail, dict):
            serializer = getattr(exc.detail, "serializer", None)
            detail = [
                {
                    "label": get_label(k.split("."), serializer),
                    "field": k,
                    "messages": handle_errors(v),
                }
                for k, v in flatten_dict(detail).items()
            ]
        else:
            messages = detail if isinstance(detail, list) else [detail]
            detail = [
                {
                    "label": NON_FIELD_ERRORS_KEY_LABEL,
                    "field": api_settings.NON_FIELD_ERRORS_KEY,
                    "messages": messages,
                }
            ]
        # Result
        response.data = OrderedDict(
            [
                ("service", get_service(context.get("view"))),
                ("error", exc.__class__.__name__),
                ("detail", detail),
            ]
        )
    return response


class CommonExceptionHandlerMixin(object):
    """Mixin to apply common exception for particular view."""

    def get_exception_handler(self):
        """Return customized exception handler."""
        return common_exception_handler

    def handle_exception(self, exc):
        """Overriding default exception handler for particular views."""
        if isinstance(
            exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)
        ):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)
            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN
        exception_handler = self.get_exception_handler()
        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)
        if response is None:
            self.raise_uncaught_exception(exc)
        response.exception = True
        return response
