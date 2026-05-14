import csv
import io
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

from htpy import a, body, button, form, h1, head, html
from htpy import input as inp
from htpy import label, li, link, table, td, th, title, tr, ul
from litestar import Litestar, MediaType, get, post
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import NotFoundException
from litestar.params import Body
from litestar.response import Redirect

from utils import HEADERS, KEYS, LABELS, fmt

LESSON_DIR = Path(__file__).parent
DB_PATH = LESSON_DIR.parent / "database" / "sightings.db"


INSERT_ROW = (
    "insert into sightings (species, sex, weight, color, datetime, latitude, longitude) "
    "values (?, ?, ?, ?, ?, ?, ?)"
)


@dataclass
class CsvUpload:
    csv_file: UploadFile


def make_app(db_path=DB_PATH):
    @get("/", media_type=MediaType.HTML)
    async def index() -> str:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("select * from sightings").fetchall()
        conn.close()
        return str(
            html(lang="en")[
                head[
                    title["Sasquatch Sightings"],
                    link(rel="stylesheet", href="/style.css"),
                ],
                body[
                    table[
                        tr[[th[col] for col in HEADERS]],
                        [
                            tr[
                                td[a(href=f"/sighting/{row['id']}")[str(row["id"])]],
                                [td[fmt(row[k])] for k in KEYS[1:]],
                            ]
                            for row in rows
                        ],
                    ],
                    ul[
                        li[a(href="/add")["Add a new sighting"]],
                        li[a(href="/upload")["Upload sightings from a CSV file"]],
                    ],
                ],
            ]
        )

    @get("/sighting/{sighting_id:int}", media_type=MediaType.HTML)
    async def detail(sighting_id: int) -> str:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "select * from sightings where id = ?", [sighting_id]
        ).fetchone()
        conn.close()
        if row is None:
            raise NotFoundException(f"No sighting with ID {sighting_id}")
        return str(
            html(lang="en")[
                head[
                    title[f"Sighting {sighting_id}"],
                    link(rel="stylesheet", href="/style.css"),
                ],
                body[
                    table[
                        [
                            tr[
                                td(class_="label")[lbl],
                                td[fmt(row[key])],
                            ]
                            for key, lbl in LABELS.items()
                        ],
                    ],
                    a(href="/")["Back to all sightings"],
                    form(method="post", action=f"/delete/{sighting_id}")[
                        button(type="submit")["Delete this sighting"],
                    ],
                ],
            ]
        )

    @post("/delete/{sighting_id:int}")
    async def delete_sighting(sighting_id: int) -> Redirect:
        conn = sqlite3.connect(db_path)
        conn.execute("delete from sightings where id = ?", [sighting_id])
        conn.commit()
        conn.close()
        return Redirect("/", status_code=303)

    @get("/add", media_type=MediaType.HTML)
    async def add_form() -> str:
        return str(
            html(lang="en")[
                head[
                    title["Add a Sighting"],
                    link(rel="stylesheet", href="/style.css"),
                ],
                body[
                    h1["Add a New Sighting"],
                    form(method="post", action="/add")[
                        label[
                            "Species", inp(type="text", name="species", required=True)
                        ],
                        label["Sex (optional)", inp(type="text", name="sex")],
                        label[
                            "Weight in kg (optional)",
                            inp(type="number", name="weight", step="0.1"),
                        ],
                        label["Color", inp(type="text", name="color", required=True)],
                        label[
                            "Date and time (YYYY-MM-DD HH:MM)",
                            inp(type="text", name="datetime", required=True),
                        ],
                        label[
                            "Latitude",
                            inp(
                                type="number",
                                name="latitude",
                                step="0.01",
                                required=True,
                            ),
                        ],
                        label[
                            "Longitude",
                            inp(
                                type="number",
                                name="longitude",
                                step="0.01",
                                required=True,
                            ),
                        ],
                        button(type="submit")["Add Sighting"],
                    ],
                    a(href="/")["Back to all sightings"],
                ],
            ]
        )

    @post("/add")
    async def add_sighting(
        data: Annotated[dict, Body(media_type=RequestEncodingType.URL_ENCODED)],
    ) -> Redirect:
        conn = sqlite3.connect(db_path)
        conn.execute(
            INSERT_ROW,
            [
                data["species"],
                data["sex"] or None,
                float(data["weight"]) if data["weight"] else None,
                data["color"],
                data["datetime"],
                float(data["latitude"]),
                float(data["longitude"]),
            ],
        )
        conn.commit()
        conn.close()
        return Redirect("/", status_code=303)

    @get("/upload", media_type=MediaType.HTML)
    async def upload_form() -> str:
        return str(
            html(lang="en")[
                head[
                    title["Upload Sightings"],
                    link(rel="stylesheet", href="/style.css"),
                ],
                body[
                    h1["Upload Sightings from a CSV File"],
                    form(
                        method="post", action="/upload", enctype="multipart/form-data"
                    )[
                        label[
                            "CSV file", inp(type="file", name="csv_file", accept=".csv")
                        ],
                        button(type="submit")["Upload"],
                    ],
                    a(href="/")["Back to all sightings"],
                ],
            ]
        )

    @post("/upload")
    async def upload_csv(
        data: Annotated[CsvUpload, Body(media_type=RequestEncodingType.MULTI_PART)],
    ) -> Redirect:
        content = await data.csv_file.read()
        reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
        conn = sqlite3.connect(db_path)
        for row in reader:
            conn.execute(
                INSERT_ROW,
                [
                    row["species"],
                    row["sex"] or None,
                    float(row["weight"]) if row["weight"] else None,
                    row["color"],
                    row["datetime"],
                    float(row["latitude"]),
                    float(row["longitude"]),
                ],
            )
        conn.commit()
        conn.close()
        return Redirect("/", status_code=303)

    @get("/style.css", media_type="text/css")
    async def styles() -> str:
        return (LESSON_DIR / "style.css").read_text()

# mccole:make-app
    return Litestar(
        [
            index,
            detail,
            delete_sighting,
            add_form,
            add_sighting,
            upload_form,
            upload_csv,
            styles,
        ]
    )


app = make_app()
# mccole:/make-app
