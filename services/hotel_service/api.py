from shared.api_client import APIClient
from shared.auth import OAuth2Handler

auth_handler = OAuth2Handler(client_id="hotel_client_id", client_secret="hotel_client_secret")
hotel_api = APIClient(base_url="https://hotel-enterprise-api.com", auth_handler=auth_handler)

def search_hotels(location: str, check_in: str, check_out: str):
    return hotel_api.get("/hotels/search", params={"location": location, "check_in": check_in, "check_out": check_out})

def book_hotel(hotel_id: str, room_type: str, guest_details: dict):
    return hotel_api.post("/hotels/book", data={"hotel_id": hotel_id, "room_type": room_type, "guest": guest_details})

def get_booking_details(booking_id: str):
    return hotel_api.get(f"/hotels/bookings/{booking_id}")

def cancel_booking(booking_id: str):
    return hotel_api.delete(f"/hotels/bookings/{booking_id}")