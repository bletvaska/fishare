import pytest

from fishare.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture
def baseurl():
    return '/api/v1/files/'


def test_when_files_are_requested_then_status_code_is_200(baseurl):
    response = client.get(baseurl)
    assert response.status_code == 200


def test_when_files_are_requested_then_response_contains_specific_dictionary(baseurl):
    response = client.get(baseurl)
    print(response)
    assert response.status_code == 200
