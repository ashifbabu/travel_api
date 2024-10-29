import requests
from shared.auth.oauth2_client import OAuth2Client
from typing import Dict, Any, Optional
from .exceptions import APIException
from .retry import retry_with_backoff
from .response import success_response, error_response
from .config import API_KEY  # If using environment variables
from .secrets_manager import get_secret  # If using AWS Secrets Manager
import re
from urllib.parse import urlparse


class APIClient:
    def __init__(self, base_url: str, oauth2_client: OAuth2Client):
        # Validate base URL format
        if not self._is_valid_url(base_url):
            raise ValueError("Invalid base URL format")

        self.base_url = base_url.rstrip("/")
        self.oauth2_client = oauth2_client
        self.session = requests.Session()
        self.api_key = API_KEY

    @retry_with_backoff(retries=3, backoff_in_seconds=1)
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.oauth2_client.get_access_token()}",
            "API-Key": API_KEY,  # If using environment variables
            # "API-Key": get_secret('your_api_key_secret_name')  # If using AWS Secrets Manager
        }

        try:
            response = self.session.request(
                method, url, json=data, params=params, headers=headers
            )
            response.raise_for_status()
            return success_response(response.json())
        except requests.RequestException as e:
            return error_response(f"API request failed: {str(e)}")

    def test_credentials(self):
        print("Testing API credentials:")
        print("API_KEY:", self.api_key)
        print("OAuth2 Token:", self.oauth2_client.get_access_token())

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        return self._make_request("DELETE", endpoint)

    def _is_valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme in ["http", "https"], result.netloc])
        except:
            return False
