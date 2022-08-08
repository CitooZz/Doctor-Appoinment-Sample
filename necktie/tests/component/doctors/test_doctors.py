from http import HTTPStatus

import pytest

from doctors.models import Doctor


@pytest.mark.django_db
def test_get_doctors(api_client, doctors_url):
    response = api_client.get(doctors_url)
    assert response.status_code == HTTPStatus.OK
    assert response.data.get("count") == 5


@pytest.mark.django_db
@pytest.mark.parametrize(
    "filter, expected_count",
    [
        ({"specialization": "1"}, 4),
        ({"language": "2"}, 1),
        ({"district": "2"}, 1),
        ({"start_price": "100", "end_price": "200"}, 1),
    ],
)
def test_valid_filters(filter, expected_count, api_client, doctors_url):
    response = api_client.get(doctors_url, data=filter)
    assert response.status_code == HTTPStatus.OK
    assert response.data["count"] == expected_count


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, sort_by",
    [
        ("name", {"sort": "-name"}),
        ("price", {"sort": "-price"}),
    ],
)
def test_ordering(
    field,
    sort_by,
    api_client,
    doctors_url,
):
    response = api_client.get(doctors_url, data=sort_by)
    doctor = Doctor.objects.order_by(sort_by["sort"]).first()

    assert response.status_code == HTTPStatus.OK
    expected_value = getattr(doctor, field)
    assert response.data["results"][0][field] == str(expected_value)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, value",
    [
        ("name", "John Doe"),
        ("address", "Mega kuningan 10"),
    ],
)
def test_search(
    field,
    value,
    api_client,
    doctors_url,
):
    search = {"search": value}
    response = api_client.get(doctors_url, data=search)

    assert response.status_code == HTTPStatus.OK
    for result in response.data["results"]:
        assert result[field] == value


@pytest.mark.django_db
@pytest.mark.parametrize(
    "filter",
    [
        {"language": "6"},
        {"specialization": "10"},
        {"district": "20"},
        {"start_price": "invalid", "end_price": "invalid"},
    ],
)
def test_invalid_filter(
    filter,
    api_client,
    doctors_url,
):
    response = api_client.get(doctors_url, data=filter)
    assert response.status_code == HTTPStatus.BAD_REQUEST
