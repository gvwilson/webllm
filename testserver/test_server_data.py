from litestar.testing import TestClient

from server_testable import make_app
from small import SMALL


def test_index_shows_both_sightings():
    with TestClient(app=make_app(SMALL)) as client:
        response = client.get("/")
    assert "/sighting/1" in response.text
    assert "/sighting/2" in response.text


def test_detail_shows_correct_species():
    with TestClient(app=make_app(SMALL)) as client:
        response = client.get("/sighting/1")
    assert "G. canadensis" in response.text


def test_none_displayed_as_empty():
    with TestClient(app=make_app(SMALL)) as client:
        response = client.get("/sighting/2")
    assert "None" not in response.text
