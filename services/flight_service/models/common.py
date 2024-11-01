from enum import Enum
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, constr

class PassengerType(str, Enum):
    ADULT = "ADT"
    CHILD = "CHD"
    INFANT = "INF"

class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"

class CabinClass(str, Enum):
    ECONOMY = "Y"
    BUSINESS = "C"
    FIRST = "F"

class Passenger(BaseModel):
    title: str
    first_name: constr(min_length=2)
    last_name: constr(min_length=2)
    pax_type: PassengerType
    date_of_birth: date
    gender: Gender
    address1: str
    address2: Optional[str] = None
    country_code: str
    nationality: str
    contact_number: str
    email: EmailStr
    is_lead_passenger: bool
    passport_number: Optional[str] = None
    passport_expiry_date: Optional[date] = None
    passport_nationality: Optional[str] = None
    ff_airline: Optional[str] = None
    ff_number: Optional[str] = None

class FlightSegment(BaseModel):
    airline: str
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    duration: str
    cabin_class: CabinClass
    available_seats: int

class PriceBreakdown(BaseModel):
    base_fare: float
    taxes: float
    total: float
    currency: str = "BDT"
