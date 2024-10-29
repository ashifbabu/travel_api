from shared.api_client import APIClient
from shared.auth import OAuth2Handler

auth_handler = OAuth2Handler(
    client_id="holiday_client_id", client_secret="holiday_client_secret"
)
holiday_api = APIClient(
    base_url="https://holiday-enterprise-api.com", auth_handler=auth_handler
)


def search_holiday_packages(destination: str, start_date: str, duration: int):
    return holiday_api.get(
        "/holidays/search",
        params={
            "destination": destination,
            "start_date": start_date,
            "duration": duration,
        },
    )


def book_holiday_package(package_id: str, traveler_details: dict):
    return holiday_api.post(
        "/holidays/book", data={"package_id": package_id, "travelers": traveler_details}
    )


def get_holiday_booking_details(booking_id: str):
    return holiday_api.get(f"/holidays/bookings/{booking_id}")


def cancel_holiday_booking(booking_id: str):
    return holiday_api.delete(f"/holidays/bookings/{booking_id}")
