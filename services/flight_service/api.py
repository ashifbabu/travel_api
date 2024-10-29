from shared.api_client import APIClient
from shared.auth import OAuth2Handler

auth_handler = OAuth2Handler(client_id="your_client_id", client_secret="your_client_secret")
flight_api = APIClient(base_url="https://flight-enterprise-api.com", auth_handler=auth_handler)

def search_flights(origin: str, destination: str, date: str):
    return flight_api.get("/flights/search", params={"origin": origin, "destination": destination, "date": date})

def book_flight(flight_id: str, passenger_details: dict):
    return flight_api.post("/flights/book", data={"flight_id": flight_id, "passenger": passenger_details})