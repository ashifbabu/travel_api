import requests
from datetime import datetime, timedelta
from typing import Any, Dict

from ..config import CLIENT_SECRET

try:
    from ..secrets_manager import get_secret  # Optional AWS Secrets Manager
except ImportError:

    def get_secret(name: str) -> str:
        return "dummy_secret_for_testing"


class OAuth2Client:
    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self._access_token = None
        self._token_expires_at = None

    def _fetch_new_token(self) -> Dict[str, Any]:
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        return response.json()

    def get_access_token(self) -> str:
        if (
            self._access_token is None
            or self._token_expires_at is None
            or datetime.now() >= self._token_expires_at
        ):
            token_data = self._fetch_new_token()
            self._access_token = token_data["access_token"]
            self._token_expires_at = datetime.now() + timedelta(
                seconds=token_data["expires_in"]
            )
        return self._access_token

    def refresh_token(self):
        # Implementation for refreshing the access token
        pass

    def is_token_expired(self):
        # Check if the current token is expired or about to expire
        pass

    # Additional methods as needed
