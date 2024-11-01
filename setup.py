from setuptools import find_packages, setup

setup(
    name="travel_api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "pydantic>=2.0.0",
        "httpx>=0.24.0",
        "pytest>=7.0.0",
        "pytest-asyncio>=0.20.0",
        "email-validator>=2.0.0",
        "redis>=4.0.0",
    ],
    python_requires=">=3.8",
)
