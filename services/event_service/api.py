from shared.api_client import APIClient
from shared.auth import OAuth2Handler

auth_handler = OAuth2Handler(client_id="event_client_id", client_secret="event_client_secret")
event_api = APIClient(base_url="https://event-enterprise-api.com", auth_handler=auth_handler)

def search_events(location: str, date: str, category: str):
    return event_api.get("/events/search", params={"location": location, "date": date, "category": category})

def book_event_tickets(event_id: str, ticket_details: dict):
    return event_api.post("/events/book", data={"event_id": event_id, "tickets": ticket_details})

def get_event_booking_details(booking_id: str):
    return event_api.get(f"/events/bookings/{booking_id}")

def cancel_event_booking(booking_id: str):
    return event_api.delete(f"/events/bookings/{booking_id}")