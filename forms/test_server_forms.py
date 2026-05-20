import sqlite3

import pytest
from starlette.testclient import TestClient

from schema import CREATE_TABLE
from server_upload import make_app
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


# mccole:count-rows
def count_rows(db_path):
    conn = sqlite3.connect(db_path)
    n = conn.execute("select count(*) from sightings").fetchone()[0]
    conn.close()
    return n
# mccole:/count-rows


# mccole:form-tests
def test_delete_removes_row(small_db):
    with TestClient(app=make_app(small_db)) as client:
        client.post("/delete/1")
    assert count_rows(small_db) == 1


def test_delete_unknown_id_is_harmless(small_db):
    with TestClient(app=make_app(small_db)) as client:
        client.post("/delete/9999")
    assert count_rows(small_db) == 2


def test_add_inserts_row(small_db):
    new_sighting = {
        "species": "G. canadensis",
        "sex": "",
        "weight": "",
        "color": "grey",
        "datetime": "2024-06-01 09:00",
        "latitude": "52.10",
        "longitude": "-118.50",
    }
    with TestClient(app=make_app(small_db)) as client:
        client.post("/add", data=new_sighting)
    assert count_rows(small_db) == 3


def test_upload_csv_inserts_rows(small_db):
    csv_content = (
        "species,sex,weight,color,datetime,latitude,longitude\n"
        "G. canadensis,Male,180,brown,2024-07-15 08:00,53.20,-117.40\n"
        "G. horribilus,,,black,2024-07-16 14:00,54.10,-116.90\n"
    )
    with TestClient(app=make_app(small_db)) as client:
        client.post(
            "/upload",
            files={"csv_file": ("upload.csv", csv_content.encode(), "text/csv")},
        )
    assert count_rows(small_db) == 4
# mccole:/form-tests
