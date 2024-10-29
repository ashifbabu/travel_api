from fastapi import APIRouter, HTTPException
import httpx
from .flyhub_adapter import prepare_flyhub_request
from .bdfare_adapter import prepare_bdfare_request
from .result_combiner import combine_results
from .auth_handler import get_auth_headers, FLYHUB_SANDBOX_URL, BDFARE_SANDBOX_URL

router = APIRouter()


@router.post("/search")
async def flight_search(search_params: dict):
    flyhub_request = prepare_flyhub_request(search_params)
    bdfare_request = prepare_bdfare_request(search_params)

    # Get authentication headers
    auth_headers = await get_auth_headers()

    # Make concurrent API calls
    async with httpx.AsyncClient() as client:
        flyhub_response = await client.post(
            f"{FLYHUB_SANDBOX_URL}AirSearch",
            json=flyhub_request,
            headers=auth_headers["flyhub"],
        )
        bdfare_response = await client.post(
            f"{BDFARE_SANDBOX_URL}AirShopping",
            json=bdfare_request,
            headers=auth_headers["bdfare"],
        )

    # Check for successful responses
    if flyhub_response.status_code != 200:
        raise HTTPException(
            status_code=flyhub_response.status_code, detail="Flyhub API request failed"
        )
    if bdfare_response.status_code != 200:
        raise HTTPException(
            status_code=bdfare_response.status_code, detail="Bdfare API request failed"
        )

    # Process and combine results
    combined_results = combine_results(flyhub_response.json(), bdfare_response.json())
    return combined_results


@router.post("/verify-price")
async def verify_price(offer_id: str):
    # TODO: Implement price verification logic
    return {"message": "Price verification not implemented yet", "offer_id": offer_id}


@router.post("/create-booking")
async def create_booking(booking_details: dict):
    # TODO: Implement booking creation logic
    return {
        "message": "Booking creation not implemented yet",
        "details": booking_details,
    }


@router.get("/{booking_id}")
async def get_booking(booking_id: str):
    # TODO: Implement booking retrieval logic
    return {
        "message": "Booking retrieval not implemented yet",
        "booking_id": booking_id,
    }


@router.get("/")
async def root():
    return {"message": "Welcome to the Flight Service API"}


@router.get("/")
async def get_flights():
    return {"message": "Flight service is working"}
