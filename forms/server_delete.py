import sqlite3
from pathlib import Path

from htpy import a, body, button, form, head, html, link, table, td, th, title, tr
from litestar import Litestar, MediaType, get, post
from litestar.exceptions import NotFoundException
from litestar.response import Redirect

LESSON_DIR = Path(__file__).parent
DB_PATH = LESSON_DIR.parent / "database" / "sightings.db"

LABELS = {
    "id": "ID",
    "species": "Species",
    "sex": "Sex",
    "weight": "Weight (kg)",
    "color": "Color",
    "datetime": "Date/Time",
    "latitude": "Latitude",
    "longitude": "Longitude",
}
HEADERS = list(LABELS.values())
KEYS = list(LABELS.keys())


def fmt(v):
    return str(v) if v is not None else ""


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

    @get("/style.css", media_type="text/css")
    async def styles() -> str:
        return (LESSON_DIR / "style.css").read_text()

    return Litestar([index, detail, delete_sighting, styles])


app = make_app()
