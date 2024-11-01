from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, constr

from .common import CabinClass, Passenger


class FlightSearchRequest(BaseModel):
    origin: constr(min_length=3, max_length=3)
    destination: constr(min_length=3, max_length=3)
    departure_date: date
    return_date: Optional[date] = None
    passengers: List[Passenger]
    cabin_class: CabinClass


class PricingRequest(BaseModel):
    search_id: str
    result_id: str


class BookingRequest(BaseModel):
    offer_id: str
    passengers: List[Passenger]


class CancelBookingRequest(BaseModel):
    booking_id: str
    reason: Optional[str] = None
