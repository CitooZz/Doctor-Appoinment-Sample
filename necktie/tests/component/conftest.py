import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

pytest_plugins = [
    "fixtures.payload",
    "fixtures.urls",
]


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        for fixture in [
            "districts",
            "languages",
            "specializations",
            "doctors",
            "openinghours",
        ]:
            call_command(
                "loaddata",
                fixture,
            )


@pytest.fixture
def api_client():
    return APIClient()
