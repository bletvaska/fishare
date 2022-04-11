from fishare import __version__
from fastapi.testclient import TestClient

from fishare.main import app


def test_version():
    assert __version__ == '0.1.0'


client = TestClient(app)


def test_when_homepage_is_retrieved_then_ok_is_returned():
    # when
    response = client.get("/")

    # then
    assert response.status_code == 200


def test_when_homepage_is_retrieved_then_content_type_is_html():
    # when
    response = client.get('/')

    # then
    assert response.headers['content-type'].startswith('text/html')
