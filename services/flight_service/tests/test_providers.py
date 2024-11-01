from datetime import date
from unittest.mock import AsyncMock, patch

import pytest

from services.flight_service.core.constants import (CabinClass, Gender,
                                                    PassengerType)
from services.flight_service.models.common import Passenger
from services.flight_service.models.request import FlightSearchRequest
from services.flight_service.providers.bdfare.client import BdfareClient
from services.flight_service.providers.flyhub.client import FlyhubClient


@pytest.mark.asyncio
@patch("services.flight_service.providers.flyhub.client.httpx.AsyncClient")
async def test_flyhub_search(mock_client):
    # Setup mock response
    mock_response = AsyncMock()
    mock_response.json.return_value = {"offers": [], "searchId": "test-search-id"}
    mock_response.raise_for_status.return_value = None
    mock_client.return_value.post.return_value = mock_response

    client = FlyhubClient()
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

    response = await client.search_flights(request)
    assert response is not None
    assert "offers" in response
