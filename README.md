drf-common-exceptions
===

| Release | CI | Coverage |
|---------|----|----------|
|[![pypi](https://img.shields.io/pypi/v/drf-common-exceptions.svg)](https://pypi.python.org/pypi/drf-common-exceptions)|[![build](https://img.shields.io/travis/com/abogoyavlensky/drf-common-exceptions.svg)](https://travis-ci.com/abogoyavlensky/drf-common-exceptions)|[![codecov](https://img.shields.io/codecov/c/github/abogoyavlensky/drf-common-exceptions.svg)](https://codecov.io/gh/abogoyavlensky/drf-common-exceptions)|

Common exception for Django REST framework. Provides single generic interface of
returning data structure for any kind of exceptions which are handled by
Django REST framework. Includes error name, path to service with line
where the error occurs and a list of actual error messages
with extended fields info.

## Requirements

- Python (3.6+)
- Django (1.11.x, 2.0+)
- Django REST Framework (3.7+)

## Installation

```bash
$ pip install drf-common-exceptions
```

## Usage examples

You can define common exception handler for whole project. Just put the
following line to your django settings inside drf section:

```
REST_FRAMEWORK = {
  ...
  "EXCEPTION_HANDLER": "drf_common_exceptions.common_exception_handler",
  ...
}
```

Or use it just for particular view or viewset:

```python
from drf_common_exceptions import CommonExceptionHandlerMixin

class MyView(CommonExceptionHandlerMixin, APIView):
    pass
```

The output will looks like for example validation error:
```json
{
    "service": "path.to.views.MyView:20",
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
```

The data structure will be the same for any other errors.

## Development

Install poetry and requirements:

```bash
$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
$ python3 -m venv path/to/venv
$ source path/to/venv/bin/activate
$ poetry install
```

Run main commands:

```bash
$ make test
$ make watch
$ make clean
$ make lint
```

Publish to pypi by default patch version:
```bash
$ make publish
```

or any level you want:
```bash
$ make publish minor
```
