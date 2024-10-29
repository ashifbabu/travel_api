from shared.api_client import APIClient
from shared.auth import OAuth2Handler

auth_handler = OAuth2Handler(client_id="train_client_id", client_secret="train_client_secret")
train_api = APIClient(base_url="https://train-enterprise-api.com", auth_handler=auth_handler)

def search_train_routes(origin: str, destination: str, date: str):
    return train_api.get("/trains/search", params={"origin": origin, "destination": destination, "date": date})

def book_train_ticket(route_id: str, passenger_details: dict):
    return train_api.post("/trains/book", data={"route_id": route_id, "passenger": passenger_details})

def get_train_booking_details(booking_id: str):
    return train_api.get(f"/trains/bookings/{booking_id}")

def cancel_train_booking(booking_id: str):
    return train_api.delete(f"/trains/bookings/{booking_id}")