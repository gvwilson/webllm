from starlette.testclient import TestClient

from server_db import make_app


def test_index_ok(small_db):
    with TestClient(app=make_app(small_db)) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "Sasquatch Sightings" in response.text


def test_index_shows_both_species(small_db):
    with TestClient(app=make_app(small_db)) as client:
        response = client.get("/")
    assert "G. canadensis" in response.text
    assert "G. horribilus" in response.text
