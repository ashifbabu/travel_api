from shared.api_client import APIClient
from shared.auth import OAuth2Handler

auth_handler = OAuth2Handler(
    client_id="insurance_client_id", client_secret="insurance_client_secret"
)
insurance_api = APIClient(
    base_url="https://insurance-enterprise-api.com", auth_handler=auth_handler
)


def get_insurance_quotes(trip_details: dict, traveler_details: dict):
    return insurance_api.post(
        "/insurance/quotes", data={"trip": trip_details, "travelers": traveler_details}
    )


def purchase_insurance(quote_id: str, payment_details: dict):
    return insurance_api.post(
        "/insurance/purchase", data={"quote_id": quote_id, "payment": payment_details}
    )


def get_insurance_policy_details(policy_id: str):
    return insurance_api.get(f"/insurance/policies/{policy_id}")


def cancel_insurance_policy(policy_id: str):
    return insurance_api.delete(f"/insurance/policies/{policy_id}")
