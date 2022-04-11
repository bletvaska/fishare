from fishare import __version__
from fastapi.testclient import TestClient

from fishare.main import app


def test_version():
    assert __version__ == '0.1.0'


client = TestClient(app)


def test_when_homepage_is_retrieved_then_ok_is_returned():
    response = client.get("/")
    assert response.status_code == 200


