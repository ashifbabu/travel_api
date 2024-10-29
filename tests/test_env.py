from dotenv import load_dotenv
import os
import pytest

# Load environment variables
load_dotenv()


def test_environment_variables():
    """Test all required environment variables are set"""
    required_vars = ["API_KEY", "CLIENT_SECRET", "CLIENT_ID", "TOKEN_URL", "BASE_URL"]

    for var in required_vars:
        value = os.getenv(var)
        print(f"{var}:", value)
        assert value is not None, f"Environment variable {var} is not set"


if __name__ == "__main__":
    test_environment_variables()
