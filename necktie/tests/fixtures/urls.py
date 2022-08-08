import pytest


@pytest.fixture()
def districts_url():
    return "/api/districts/"


@pytest.fixture()
def languages_url():
    return "/api/languages/"


@pytest.fixture()
def specializations_url():
    return "/api/specializations/"


@pytest.fixture()
def doctors_url():
    return "/api/doctors/"


@pytest.fixture()
def detail_doctor_url():
    return "/api/doctors/{doctor_id}/"
