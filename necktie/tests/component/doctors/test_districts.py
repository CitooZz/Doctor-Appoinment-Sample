from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_districts(api_client, districts_url):
    response = api_client.get(districts_url)
    assert response.status_code == HTTPStatus.OK
    assert response.data.get("count") == 3
