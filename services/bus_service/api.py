from shared.api_client import APIClient
from shared.auth import OAuth2Handler

auth_handler = OAuth2Handler(
    client_id="bus_client_id", client_secret="bus_client_secret"
)
bus_api = APIClient(
    base_url="https://bus-enterprise-api.com", auth_handler=auth_handler
)


def search_bus_routes(origin: str, destination: str, date: str):
    return bus_api.get(
        "/buses/search",
        params={"origin": origin, "destination": destination, "date": date},
    )


def book_bus_ticket(route_id: str, passenger_details: dict):
    return bus_api.post(
        "/buses/book", data={"route_id": route_id, "passenger": passenger_details}
    )


def get_bus_booking_details(booking_id: str):
    return bus_api.get(f"/buses/bookings/{booking_id}")


def cancel_bus_booking(booking_id: str):
    return bus_api.delete(f"/buses/bookings/{booking_id}")
