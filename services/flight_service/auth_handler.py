import httpx
import os
from fastapi import HTTPException

FLYHUB_SANDBOX_URL = "http://api.sandbox.flyhub.com/api/v1/"
BDFARE_SANDBOX_URL = "https://bdf.centralindia.cloudapp.azure.com/api/enterprise/"

FLYHUB_USERNAME = os.getenv("FLYHUB_USERNAME")
FLYHUB_API_KEY = os.getenv("FLYHUB_API_KEY")
BDFARE_API_KEY = os.getenv("BDFARE_API_KEY")

async def get_flyhub_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FLYHUB_SANDBOX_URL}Authenticate",
            json={"username": FLYHUB_USERNAME, "apikey": FLYHUB_API_KEY}
        )
        if response.status_code == 200:
            return response.json()["TokenId"]
        raise HTTPException(status_code=401, detail="Failed to authenticate with Flyhub")

def get_bdfare_headers():
    return {"Authorization": f"Bearer {BDFARE_API_KEY}"}

async def get_auth_headers():
    flyhub_token = await get_flyhub_token()
    return {
        "flyhub": {"Authorization": f"Bearer {flyhub_token}"},
        "bdfare": get_bdfare_headers()
    }