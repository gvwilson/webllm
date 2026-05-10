from litestar.testing import TestClient

from server4 import make_app

SMALL = [
    {
        "id": 1,
        "species": "G. canadensis",
        "sex": "Female",
        "weight": 142,
        "color": "dark brown",
        "datetime": "2024-01-08 07:14",
        "latitude": 49.23,
        "longitude": -121.45,
    },
    {
        "id": 2,
        "species": "G. horribilus",
        "sex": None,
        "weight": None,
        "color": "black",
        "datetime": "2024-01-19 14:32",
        "latitude": 50.71,
        "longitude": -119.38,
    },
]


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
