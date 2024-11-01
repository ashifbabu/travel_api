from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from .common import FlightSegment, PriceBreakdown, Passenger
from ..core.constants import BookingStatus

class FlightOffer(BaseModel):
    offer_id: str
    provider: str
    segments: List[FlightSegment]
    price: PriceBreakdown
    refundable: bool
    available_seats: int

class FlightSearchResponse(BaseModel):
    offers: List[FlightOffer] = []
    currency: str = "BDT"
    search_id: str

class BookingResponse(BaseModel):
    booking_id: str
    pnr: str
    status: BookingStatus
    segments: List[FlightSegment]
    passengers: List[Passenger]
    price: PriceBreakdown
    created_at: datetime
    expires_at: Optional[datetime] = None

class PricingResponse(BaseModel):
    offer_id: str
    price: PriceBreakdown
    is_price_changed: bool
    is_available: bool

class CancelBookingResponse(BaseModel):
    booking_id: str
    status: BookingStatus
    cancellation_fee: Optional[float] = None
    refund_amount: Optional[float] = None
    message: str