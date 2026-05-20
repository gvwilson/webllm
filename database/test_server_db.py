import sqlite3

import pytest
from starlette.testclient import TestClient

from schema import CREATE_TABLE
from server_db import make_app
from small import SMALL

INSERT_ROW = "insert into sightings values (?, ?, ?, ?, ?, ?, ?, ?)"


@pytest.fixture
def small_db(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    conn.execute(CREATE_TABLE)
    for s in SMALL:
        conn.execute(
            INSERT_ROW,
            [
                s["id"],
                s["species"],
                s["sex"],
                s["weight"],
                s["color"],
                s["datetime"],
                s["latitude"],
                s["longitude"],
            ],
        )
    conn.commit()
    conn.close()
    return db_path


def test_index_ok(small_db):
    with TestClient(app=make_app(small_db)) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "Sasquatch Sightings" in response.text


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
