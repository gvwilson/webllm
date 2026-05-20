from starlette.testclient import TestClient

from server_db import make_app


def test_detail_ok(small_db):
    with TestClient(app=make_app(small_db)) as client:
        response = client.get("/sighting/1")
    assert response.status_code == 200
    assert "G. canadensis" in response.text


def test_missing_sighting(small_db):
    with TestClient(app=make_app(small_db)) as client:
        response = client.get("/sighting/9999")
    assert response.status_code == 404


def test_none_displayed_as_empty(small_db):
    with TestClient(app=make_app(small_db)) as client:
        response = client.get("/sighting/2")
    assert response.status_code == 200
    assert "None" not in response.text
