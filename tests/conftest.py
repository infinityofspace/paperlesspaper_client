import pytest

from paperlesspaper_client.client import Client


@pytest.fixture
def client() -> Client:
    return Client("test-api-key")


@pytest.fixture
def base_url() -> str:
    return "https://api.paperlesspaper.de/v1/"
