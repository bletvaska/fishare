import pytest
from fastapi.testclient import TestClient

from fishare.main import app

pytestmark = [pytest.mark.api, pytest.mark.files]


@pytest.fixture(scope="session")
def client():
    yield TestClient(app)


def test_when_files_are_retrieved_then_content_type_should_be_json(client):
    response = client.get("/api/v1/files/")
    assert response.headers["content-type"] == "application/json"


def test_when_files_are_retrieved_then_http_status_code_should_be_ok(client):
    response = client.get("/api/v1/files/")
    assert response.status_code == 200


def test_when_files_are_retrieved_then_list_is_returned(client):
    response = client.get("/api/v1/files/")
    payload = response.json()
    assert type(payload) == list
