from shared.api_client import APIClient
from shared.auth import OAuth2Handler

auth_handler = OAuth2Handler(client_id="car_rental_client_id", client_secret="car_rental_client_secret")
car_rental_api = APIClient(base_url="https://car-rental-enterprise-api.com", auth_handler=auth_handler)

def search_cars(location: str, pickup_date: str, return_date: str):
    return car_rental_api.get("/cars/search", params={"location": location, "pickup_date": pickup_date, "return_date": return_date})

def reserve_car(car_id: str, rental_details: dict):
    return car_rental_api.post("/cars/reserve", data={"car_id": car_id, "rental": rental_details})

def get_reservation_details(reservation_id: str):
    return car_rental_api.get(f"/cars/reservations/{reservation_id}")

def cancel_reservation(reservation_id: str):
    return car_rental_api.delete(f"/cars/reservations/{reservation_id}")