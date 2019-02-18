from drf_common_exceptions import common_exception_handler
from rest_framework.exceptions import APIException


def test_common_exception_handler_if_error_without_detail(mocker):
    exp = APIException({"data": "test"})
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data["service"] == "unittest.mock.Mock:"
    assert response.data["error"] == "APIException"
    assert response.data["detail"][0]["messages"] == ["test"]
