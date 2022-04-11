import pytest
from faker import Faker

from fastapi.testclient import TestClient

from fishare.main import app

client = TestClient(app)
faker = Faker()


def test_when_no_arguments_are_given_then_return_ok():
    response = client.get('/api/v1/files/')
    assert response.status_code == 200


def test_when_no_arguments_are_given_then_return_json():
    response = client.get('/api/v1/files/')
    assert response.json()


@pytest.mark.parametrize('key', ['count', 'first', 'last', 'next', 'previous', 'results'])
def test_when_no_arguments_are_given_then_response_should_contain_specific_keys(key: str):
    response = client.get('/api/v1/files/')
    payload = response.json()
    assert key in payload


def test_when_first_page_is_accessed_then_previous_link_is_none():
    response = client.get('/api/v1/files/')
    payload = response.json()
    assert payload['previous'] is None


@pytest.mark.parametrize('slug', ['Raw5CUYb', 'q36s5Tyg', '9OraDu_T'])
def test_when_file_with_specific_slug_is_retrieved_then_such_slug_is_in_response(slug):
    response = client.get(f'/api/v1/files/{slug}')
    payload = response.json()
    assert payload['slug'] == slug


@pytest.mark.parametrize('_', range(10))
def test_when_invalid_token_given_then_return_not_found(_):
    slug = faker.word()
    response = client.get(f'/api/v1/files/{slug}')
    assert response.status_code == 404


@pytest.mark.parametrize('key', ['detail', 'instance', 'status', 'title', 'type'])
def test_when_invalid_token_is_given_then_response_should_contain_specific_keys(key: str):
    slug = faker.word()
    response = client.get(f'/api/v1/files/{slug}')
    payload = response.json()
    assert key in payload
