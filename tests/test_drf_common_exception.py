import pytest
from rest_framework.exceptions import (APIException, NotAuthenticated,
                                       ValidationError)
from rest_framework.mixins import Response

from drf_common_exceptions.exceptions import (CommonExceptionHandlerMixin,
                                              common_exception_handler,
                                              get_label)


def test_common_exception_handler_if_error_without_detail(mocker):
    exp = APIException({"data": "test"})
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data["service"] == "unittest.mock.Mock:"
    assert response.data["error"] == "APIException"
    assert response.data["detail"][0]["messages"] == ["test"]


def test_common_exception_handler_if_error_is_list_of_string(mocker):
    exp = APIException(["testing error"])
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data["service"] == "unittest.mock.Mock:"
    assert response.data["error"] == "APIException"
    assert response.data["detail"][0]["messages"] == ["testing error"]


def test_common_exception_handler_if_error_is_string(mocker):
    exp = APIException("testing error")
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data["service"] == "unittest.mock.Mock:"
    assert response.data["error"] == "APIException"
    assert response.data["detail"][0]["messages"] == ["testing error"]
    assert response.data["detail"][0]["field"] == "non_field_errors"


def test_common_exception_handler_if_error_is_nested_dict(mocker):
    exp = ValidationError({"foo": {"bar": "testing error"}})
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data["service"] == "unittest.mock.Mock:"
    assert response.data["error"] == "ValidationError"
    assert response.data["detail"][0]["field"] == "foo.bar"
    assert response.data["detail"][0]["messages"] == ["testing error"]


def test_common_exception_handler_if_error_is_common(mocker):
    exp = APIException({"non_field_errors": "test"})
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data["service"] == "unittest.mock.Mock:"
    assert response.data["error"] == "APIException"
    assert response.data["detail"][0]["messages"] == ["test"]
    assert response.data["detail"][0]["label"] is None


def test_handle_exception_with_basic_exception_ok(mocker, rf, view):
    view.request = rf.get("")
    view.request.data = {}
    response = view.handle_exception(APIException("test"))
    assert isinstance(response, Response)
    assert "tests.conftest.TestingView" in response.data["service"]
    assert "APIException" == response.data["error"]


def test_handle_exception_with_not_auth_exception_ok(mocker, rf, view):
    view.request = rf.get("")
    view.request.data = {}
    response = view.handle_exception(NotAuthenticated("test"))
    assert isinstance(response, Response)
    assert response.status_code == 403
    assert "NotAuthenticated" == response.data["error"]


def test_handle_exception_with_auth_headers_ok(mocker, rf, view):
    view.request = rf.get("")
    view.request.data = {}
    mocker.patch.object(view, "get_authenticate_header", return_value=True)
    response = view.handle_exception(NotAuthenticated("test"))
    assert response._headers["www-authenticate"] == (
        "WWW-Authenticate",
        "True",
    )


def test_exception_handler_returns_empty_response_ok(mocker, rf, view):
    view.request = rf.get("")
    view.request.data = {}
    mocker.patch.object(
        view,
        "get_exception_handler",
        return_value=mocker.Mock(return_value=None),
    )
    with pytest.raises(RuntimeError):
        response = view.handle_exception(APIException("test"))


def test_get_label_first_level_ok(serializer):
    label = get_label(['name'], serializer)
    assert label == 'Name'


def test_get_label_second_level_ok(serializer):
    label = get_label(['name', 'first_name'], serializer)
    assert label == 'First name'


def test_get_label_non_field_errors_ok(serializer):
    label = get_label(["non_field_errors"], serializer)
    assert label == None
