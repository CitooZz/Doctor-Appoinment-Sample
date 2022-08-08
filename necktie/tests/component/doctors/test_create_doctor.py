from http import HTTPStatus

from django.utils.translation import ugettext_lazy as _
import pytest

from doctors.models import Doctor


@pytest.mark.django_db
def test_create_doctor_success(api_client, doctors_url, create_doctor_payload):
    response = api_client.post(doctors_url, data=create_doctor_payload)
    assert response.status_code == HTTPStatus.CREATED
    assert response.data.get("id")
    assert Doctor.objects.count() == 6


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field",
    [
        "name",
        "opening_hours",
        "price",
        "address",
        "specialization",
        "district",
        "language",
    ],
)
def test_missing_fields(
    field,
    api_client,
    doctors_url,
    create_doctor_payload,
):
    del create_doctor_payload[field]
    response = api_client.post(doctors_url, data=create_doctor_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data.get(field) == ["This field is required."]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, error_code",
    [
        ("name", "This field may not be blank."),
        (
            "opening_hours",
            {"non_field_errors": ["This list may not be empty."]},
        ),
        ("price", "A valid number is required."),
        ("address", "This field may not be blank."),
        ("specialization", "This field may not be null."),
        ("district", "This field may not be null."),
        ("language", "This field may not be null."),
    ],
)
def test_blank_fields(
    field,
    error_code,
    api_client,
    doctors_url,
    create_doctor_payload,
):
    create_doctor_payload[field] = ""
    if field == "opening_hours":
        create_doctor_payload[field] = []

    response = api_client.post(doctors_url, data=create_doctor_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    expected_error = [error_code] if field != "opening_hours" else error_code
    assert response.data.get(field) == expected_error


@pytest.mark.django_db
def test_overlapping_opening_hours(api_client, doctors_url, create_doctor_payload):
    create_doctor_payload["opening_hours"].append(
        {
            "weekday": "Sunday",
            "start_hour": "15:30",
            "end_hour": "17:00",
        }
    )
    response = api_client.post(doctors_url, data=create_doctor_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert str(_("Opening hour is overlapping.")) in str(response.content)


@pytest.mark.django_db
def test_duplicate_opening_hours(api_client, doctors_url, create_doctor_payload):
    create_doctor_payload["opening_hours"].append(
        {
            "weekday": "Sunday",
            "start_hour": "15:00",
            "end_hour": "16:00",
        }
    )
    response = api_client.post(doctors_url, data=create_doctor_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert str(_("Duplicate opening hour.")) in str(response.content)


@pytest.mark.django_db
def test_greater_start_hour(api_client, doctors_url, create_doctor_payload):
    create_doctor_payload["opening_hours"].append(
        {
            "weekday": "Sunday",
            "start_hour": "18:00",
            "end_hour": "16:00",
        }
    )
    response = api_client.post(doctors_url, data=create_doctor_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert str(_("End hour should be greater than start hour.")) in str(
        response.content
    )
