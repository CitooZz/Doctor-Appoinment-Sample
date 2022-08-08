from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_specializations(api_client, specializations_url):
    response = api_client.get(specializations_url)
    assert response.status_code == HTTPStatus.OK
    assert response.data.get("count") == 3
