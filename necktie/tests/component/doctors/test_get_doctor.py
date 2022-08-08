from http import HTTPStatus

import pytest

from doctors.models import Doctor


@pytest.mark.django_db
def test_get_detail_success(api_client, detail_doctor_url):
    doctor = Doctor.objects.first()
    response = api_client.get(detail_doctor_url.format(doctor_id=doctor.id))
    assert response.status_code == HTTPStatus.OK
    assert doctor.id == response.data.get("id")
    assert doctor.name == response.data.get("name")


@pytest.mark.django_db
def test_get_detail_not_found(api_client, detail_doctor_url):
    response = api_client.get(detail_doctor_url.format(doctor_id=10))
    assert response.status_code == HTTPStatus.NOT_FOUND
