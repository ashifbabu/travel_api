from datetime import date, datetime
from unittest.mock import AsyncMock

import pytest

from services.flight_service.core.constants import (CabinClass, Gender,
                                                    PassengerType,
                                                    ProviderName)
from services.flight_service.models.common import (FlightSegment, Passenger,
                                                   PriceBreakdown)
from services.flight_service.models.request import FlightSearchRequest
from services.flight_service.models.response import (FlightOffer,
                                                     FlightSearchResponse)
from services.flight_service.services.flight_service import FlightService


@pytest.fixture
def flight_service():
    service = FlightService()
    service.cache = AsyncMock()
    service.cache.get.return_value = None
    return service


@pytest.mark.asyncio
async def test_search_flights(flight_service):
    # Create mock flight offer
    mock_offer = FlightOffer(
        offer_id="test-offer",
        provider="flyhub",
        segments=[
            FlightSegment(
                airline="BG",
                flight_number="123",
                departure_airport="DAC",
                arrival_airport="DXB",
                departure_time=datetime.now(),
                arrival_time=datetime.now(),
                duration="2h",
                cabin_class=CabinClass.ECONOMY,
                available_seats=10,
            )
        ],
        price=PriceBreakdown(base_fare=100.0, taxes=20.0, total=120.0),
        refundable=True,
        available_seats=10,
    )

    # Mock response data
    mock_response = FlightSearchResponse(
        offers=[mock_offer], currency="BDT", search_id="test-search-id"
    )

    # Mock provider client
    mock_provider = AsyncMock()
    mock_provider.search_flights.return_value = mock_response

    # Set up mock providers - Only use one provider for test
    flight_service.providers = {ProviderName.FLYHUB: mock_provider}

    # Create test request
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

    # Test search
    response = await flight_service.search_flights(
        request, providers=[ProviderName.FLYHUB]
    )
    assert isinstance(response, FlightSearchResponse)
    assert response.currency == "BDT"
    assert len(response.offers) == 1
