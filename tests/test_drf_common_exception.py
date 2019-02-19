from drf_common_exceptions import common_exception_handler
from rest_framework.exceptions import APIException


def test_common_exception_handler_if_error_without_detail(mocker):
    exp = APIException({"data": "test"})
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data["service"] == "unittest.mock.Mock:"
    assert response.data["error"] == "APIException"
    assert response.data["detail"][0]["messages"] == ["test"]


def test_common_exception_handler_if_error_is_list_of_string(mocker):
    exp = APIException(['testing error'])
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data['service'] == 'unittest.mock.Mock:'
    assert response.data['error'] == 'APIException'
    assert response.data['detail'][0]['messages'] == ['testing error']


def test_common_exception_handler_if_error_is_string(mocker):
    exp = APIException('testing error')
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data['service'] == 'unittest.mock.Mock:'
    assert response.data['error'] == 'APIException'
    assert response.data['detail'][0]['messages'] == ['testing error']
    assert response.data['detail'][0]['field'] == 'none_field_errors'


def test_common_exception_handler_if_error_is_nested_dict(mocker):
    exp = APIException({'foo': {'bar': 'testing error'}})
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data['service'] == 'unittest.mock.Mock:'
    assert response.data['error'] == 'APIException'
    assert response.data['detail'][0]['field'] == 'foo.bar'
    assert response.data['detail'][0]['messages'] == ['testing error']


def test_common_exception_handler_if_error_is_common(mocker):
    exp = APIException({'non_field_errors': 'test'})
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data['service'] == 'unittest.mock.Mock:'
    assert response.data['error'] == 'APIException'
    assert response.data['detail'][0]['messages'] == ['test']
    assert response.data['detail'][0]['label'] is None
