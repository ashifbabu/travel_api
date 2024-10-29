import pytest

from shared.api_client import APIClient
from shared.auth.oauth2_client import OAuth2Client


@pytest.fixture
def oauth2_client():
    """Fixture for OAuth2Client"""
    return OAuth2Client(
        client_id="test_client_id", token_url="https://test.com/oauth/token"
    )


@pytest.fixture
def api_client(oauth2_client):
    """Fixture for APIClient"""
    return APIClient(base_url="https://test.com/api", oauth2_client=oauth2_client)
