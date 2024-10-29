import pytest
import responses
import requests  # Add this import
from unittest.mock import patch, Mock
import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared.api_client import APIClient
from shared.auth.oauth2_client import OAuth2Client

# Load environment variables
load_dotenv()

# Remove the global client initialization and test_credentials call
# This should be handled in individual tests instead


class MockRetryWithBackoff:
    def __call__(self, *args, **kwargs):
        def decorator(func):
            return func

        return decorator


@pytest.fixture
def oauth2_client():
    mock_oauth2_client = Mock(spec=OAuth2Client)
    mock_oauth2_client.get_access_token.return_value = "test_token"
    return mock_oauth2_client


@pytest.fixture
def api_client(oauth2_client):
    return APIClient("https://api.example.com", oauth2_client)


# Add a new test for credentials initialization
@responses.activate
def test_credentials_initialization():
    responses.add(
        responses.POST,
        "https://test.com/oauth/token",
        json={"access_token": "test_token", "expires_in": 3600},
        status=200,
    )

    oauth2_client = OAuth2Client(
        client_id="test_client_id",
        client_secret="test_client_secret",
        token_url="https://test.com/oauth/token",
    )

    api_client = APIClient(base_url="https://test.com/api", oauth2_client=oauth2_client)

    # Now test_credentials() should work with mocked response
    api_client.test_credentials()


# Test basic HTTP methods
@patch("shared.api_client.retry_with_backoff", MockRetryWithBackoff())
@responses.activate
def test_get_request_success(api_client):
    responses.add(
        responses.GET, "https://api.example.com/test", json={"key": "value"}, status=200
    )

    response = api_client.get("/test")
    assert response == {"status": "success", "data": {"key": "value"}}


@patch("shared.api_client.retry_with_backoff", MockRetryWithBackoff())
@responses.activate
def test_get_request_error(api_client):
    responses.add(
        responses.GET,
        "https://api.example.com/test",
        json={"error": "Not found"},
        status=404,
    )

    response = api_client.get("/test")
    assert response == {
        "status": "error",
        "errors": [
            "API request failed: 404 Client Error: Not Found for url: https://api.example.com/test"
        ],
    }


@patch("shared.api_client.retry_with_backoff", MockRetryWithBackoff())
@responses.activate
def test_post_request_success(api_client):
    responses.add(
        responses.POST, "https://api.example.com/test", json={"id": "123"}, status=201
    )

    response = api_client.post("/test", data={"name": "Test"})
    assert response == {"status": "success", "data": {"id": "123"}}


@patch("shared.api_client.retry_with_backoff", MockRetryWithBackoff())
@responses.activate
def test_put_request_success(api_client):
    responses.add(
        responses.PUT,
        "https://api.example.com/test/123",
        json={"id": "123", "name": "Updated"},
        status=200,
    )

    response = api_client.put("/test/123", data={"name": "Updated"})
    assert response == {"status": "success", "data": {"id": "123", "name": "Updated"}}


@patch("shared.api_client.retry_with_backoff", MockRetryWithBackoff())
@responses.activate
def test_delete_request_success(api_client):
    responses.add(
        responses.DELETE,
        "https://api.example.com/test/123",
        json={"message": "Deleted"},
        status=200,
    )

    response = api_client.delete("/test/123")
    assert response == {"status": "success", "data": {"message": "Deleted"}}


# Test OAuth2 functionality
@responses.activate
def test_oauth2_client():
    token_url = "https://auth.example.com/token"
    client_id = "test_client_id"
    client_secret = "test_client_secret"

    responses.add(
        responses.POST,
        token_url,
        json={"access_token": "new_test_token", "expires_in": 3600},
        status=200,
    )

    oauth2_client = OAuth2Client(client_id, client_secret, token_url)
    token = oauth2_client.get_access_token()

    assert token == "new_test_token"
    assert (
        responses.calls[0].request.body
        == f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
    )


@responses.activate
def test_oauth2_integration():
    # Mock the token endpoint
    responses.add(
        responses.POST,
        "https://auth.example.com/token",
        json={"access_token": "test_access_token", "expires_in": 3600},
        status=200,
    )

    # Mock an API endpoint
    responses.add(
        responses.GET,
        "https://api.example.com/protected-resource",
        json={"data": "protected content"},
        status=200,
        match=[
            responses.matchers.header_matcher(
                {"Authorization": "Bearer test_access_token"}
            )
        ],
    )

    # Create OAuth2Client and APIClient instances
    oauth2_client = OAuth2Client(
        client_id="test_client_id",
        client_secret="test_client_secret",
        token_url="https://auth.example.com/token",
    )
    api_client = APIClient("https://api.example.com", oauth2_client)

    # Make a request to the protected resource
    response = api_client.get("/protected-resource")

    # Assertions
    assert response["status"] == "success"
    assert response["data"] == {"data": "protected content"}

    # Verify that two requests were made (one for token, one for the API call)
    assert len(responses.calls) == 2

    # Verify the token request
    token_request = responses.calls[0].request
    assert token_request.url == "https://auth.example.com/token"
    assert "client_id=test_client_id" in token_request.body
    assert "client_secret=test_client_secret" in token_request.body

    # Verify the API request
    api_request = responses.calls[1].request
    assert api_request.url == "https://api.example.com/protected-resource"
    assert api_request.headers["Authorization"] == "Bearer test_access_token"


# Test error handling and edge cases
@patch("shared.api_client.retry_with_backoff", MockRetryWithBackoff())
@responses.activate
def test_network_error(api_client):
    # Use responses.CallbackResponse to simulate a network error
    def request_callback(request):
        raise requests.exceptions.ConnectionError("Network error")

    responses.add_callback(
        responses.GET, "https://api.example.com/test", callback=request_callback
    )

    response = api_client.get("/test")
    assert response["status"] == "error"
    assert "Network error" in str(response["errors"][0])


@patch("shared.api_client.retry_with_backoff", MockRetryWithBackoff())
@responses.activate
def test_invalid_json_response(api_client):
    responses.add(
        responses.GET, "https://api.example.com/test", body="Invalid JSON", status=200
    )

    response = api_client.get("/test")
    assert response["status"] == "error"


def test_invalid_base_url(oauth2_client):
    invalid_urls = [
        "invalid_url",
        "http:/invalid.com",
        "ftp://invalid.com",
        "not_a_url",
    ]

    for url in invalid_urls:
        with pytest.raises(ValueError, match=r"Invalid base URL format"):
            APIClient(url, oauth2_client)


@responses.activate
def test_token_refresh():
    # Mock initial token request
    responses.add(
        responses.POST,
        "https://auth.example.com/token",
        json={"access_token": "initial_token", "expires_in": 0},
        status=200,
    )

    # Mock refresh token request
    responses.add(
        responses.POST,
        "https://auth.example.com/token",
        json={"access_token": "refreshed_token", "expires_in": 3600},
        status=200,
    )

    oauth2_client = OAuth2Client(
        client_id="test_client_id",
        client_secret="test_client_secret",
        token_url="https://auth.example.com/token",
    )

    # First call should get initial token
    token1 = oauth2_client.get_access_token()
    assert token1 == "initial_token"

    # Second call should get refreshed token because the first one expired
    token2 = oauth2_client.get_access_token()
    assert token2 == "refreshed_token"


if __name__ == "__main__":
    pytest.main(["-v", "-s"])
