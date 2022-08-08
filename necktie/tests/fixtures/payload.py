import pytest


@pytest.fixture()
def create_doctor_payload():
    return {
        "opening_hours": [
            {
                "weekday": "Public Holiday",
                "start_hour": None,
                "end_hour": None,
                "is_closed": True,
            },
            {
                "weekday": "Sunday",
                "start_hour": "15:00",
                "end_hour": "16:00",
            },
        ],
        "name": "test doctor",
        "price": "200",
        "is_price_inclusive": True,
        "address": "string",
        "specialization": 1,
        "district": 1,
        "language": 1,
    }
