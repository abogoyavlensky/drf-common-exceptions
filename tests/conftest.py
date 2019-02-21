import pytest


def pytest_configure():
    from django.conf import settings

    settings.configure()
    try:
        import django

        django.setup()
    except AttributeError:
        pass


@pytest.fixture
def view():
    from rest_framework.views import APIView
    from drf_common_exceptions.exceptions import CommonExceptionHandlerMixin

    class TestingView(CommonExceptionHandlerMixin, APIView):
        pass

    return TestingView()


@pytest.fixture
def serializer():
    from rest_framework import serializers

    class NameSerializer(serializers.Serializer):
        first_name = serializers.CharField(label="First name")
        last_name = serializers.CharField(label="Last name")

    class TestingSerializer(serializers.Serializer):
        name = NameSerializer()

    return TestingSerializer()
