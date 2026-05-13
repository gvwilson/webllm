import sqlite3

import pytest

from schema import CREATE_TABLE
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
