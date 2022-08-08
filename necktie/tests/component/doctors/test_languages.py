from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_languages(api_client, languages_url):
    response = api_client.get(languages_url)
    assert response.status_code == HTTPStatus.OK
    assert response.data.get("count") == 2
