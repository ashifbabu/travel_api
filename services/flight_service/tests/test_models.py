from datetime import date, datetime

import pytest

from services.flight_service.core.constants import (CabinClass, Gender,
                                                    PassengerType)
from services.flight_service.models.common import Passenger
from services.flight_service.models.request import (BookingRequest,
                                                    FlightSearchRequest)


def test_flight_search_request():
    # Test valid request
    request = FlightSearchRequest(
        origin="DAC",
        destination="DXB",
        departure_date=date(2024, 4, 1),
        passengers=[
            Passenger(
                title="Mr",
                first_name="John",
                last_name="Doe",
                pax_type=PassengerType.ADULT,
                date_of_birth=date(1990, 1, 1),
                gender=Gender.MALE,
                address1="123 Street",
                country_code="BD",
                nationality="BD",
                contact_number="1234567890",
                email="john@example.com",
                is_lead_passenger=True,
            )
        ],
        cabin_class=CabinClass.ECONOMY,
    )
    assert request.origin == "DAC"
    assert request.destination == "DXB"
    assert len(request.passengers) == 1

    # Test invalid request
    with pytest.raises(ValueError):
        FlightSearchRequest(
            origin="INVALID",  # Too long
            destination="DXB",
            departure_date=date(2024, 4, 1),
            passengers=[],  # Empty passengers list
        )
