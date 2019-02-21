drf-common-exceptions
===

<!-- TODO: add labels as table -->

Common exception for Django REST framework. Produces single generic interface of
returning data structure for any kind of exceptions which are processed by
Django REST framework. Includes error name, path to service with line
where the error occurs and a list of actual error messages
with extended fields info.

<!-- TODO: documentation link -->

## Requirements

- Python (3.5+)
- Django (1.11.x, 2+)
- Django REST Framework (3.7+)

## Installation

```bash
$ pip install drf-common-exceptions
```

## Usage examples

You can define common exception handler for whole project. Just put the
following line to your django settings inside drf section:

```json
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

<!-- TODO: add info about configuration when it will be added -->

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
