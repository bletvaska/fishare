import pytest

from fishare.main import app
from fastapi.testclient import TestClient

from fishare.models.pager import Pager

client = TestClient(app)


@pytest.fixture
def baseurl():
    return '/api/v1/files/'


@pytest.fixture
def empty_db():
    pass


@pytest.fixture
def no_db():
    pass


@pytest.fixture
def random_db():
    pass


def test_when_files_are_requested_then_status_code_is_200(baseurl):
    response = client.get(baseurl)
    assert response.status_code == 200


def test_when_files_are_requested_then_response_is_of_type_pager(baseurl):
    response = client.get(baseurl)
    Pager(**response.json())


def test_when_no_offset_is_given_then_previous_is_null(baseurl):
    response = client.get(baseurl)
    pager = Pager(**response.json())
    assert pager.previous is None
