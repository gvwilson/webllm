from litestar.testing import TestClient

from server4 import make_app


def test_index_returns_ok():
    with TestClient(app=make_app()) as client:
        response = client.get("/")
    assert response.status_code == 200


def test_index_contains_title():
    with TestClient(app=make_app()) as client:
        response = client.get("/")
    assert "Sasquatch Sightings" in response.text


def test_detail_returns_ok():
    with TestClient(app=make_app()) as client:
        response = client.get("/sighting/1")
    assert response.status_code == 200


def test_missing_sighting_returns_404():
    with TestClient(app=make_app()) as client:
        response = client.get("/sighting/9999")
    assert response.status_code == 404
