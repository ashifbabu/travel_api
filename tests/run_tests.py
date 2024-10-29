import os
import sys

import pytest


def run_tests():
    """Run all tests with coverage report"""
    # Add project root to Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    # Run pytest with coverage
    pytest.main(["--cov=shared", "--cov-report=term-missing", "-v", "tests/"])


if __name__ == "__main__":
    run_tests()
