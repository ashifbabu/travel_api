import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables with fallbacks
API_KEY = os.getenv("API_KEY", "default_api_key")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "default_client_secret")
CLIENT_ID = os.getenv("CLIENT_ID", "default_client_id")
TOKEN_URL = os.getenv("TOKEN_URL", "https://api.example.com/oauth/token")
BASE_URL = os.getenv("BASE_URL", "https://api.example.com")
