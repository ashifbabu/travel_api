import pytest
from datetime import date
from services.flight_service.utils.cache import Cache
from services.flight_service.utils.validators import validate_search_request, validate_passenger
from services.flight_service.models.request import FlightSearchRequest
from services.flight_service.models.common import Passenger
from services.flight_service.core.constants import PassengerType, Gender, CabinClass

@pytest.mark.asyncio
async def test_cache():
    cache = Cache()
    key = "test_key"
    value = {"test": "data"}
    
    # Test set
    success = await cache.set(key, value)
    assert success is True
    
    # Test get
    cached_value = await cache.get(key)
    assert cached_value == value
    
    # Test delete
    success = await cache.delete(key)
    assert success is True
    
    # Test get after delete
    cached_value = await cache.get(key)
    assert cached_value is None

def test_validators():
    # Test search request validation
    request = FlightSearchRequest(
        origin="DAC",
        destination="DAC",  # Same as origin
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
                is_lead_passenger=True
            )
        ],
        cabin_class=CabinClass.ECONOMY
    )
    errors = validate_search_request(request)
    assert len(errors) > 0
    assert "Origin and destination cannot be the same" in errors

    # Test passenger validation with valid email
    passenger = Passenger(
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
        is_lead_passenger=True
    )
    errors = validate_passenger(passenger)
    assert len(errors) == 0

    # Test passenger validation with invalid data
    with pytest.raises(ValueError):
        Passenger(
            title="Mr",
            first_name="J",  # Too short
            last_name="Doe",
            pax_type=PassengerType.ADULT,
            date_of_birth=date(1990, 1, 1),
            gender=Gender.MALE,
            address1="123 Street",
            country_code="BD",
            nationality="BD",
            contact_number="1234567890",
            email="invalid-email",  # Invalid email
            is_lead_passenger=True
        )