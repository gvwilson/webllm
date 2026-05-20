import sqlite3
from pathlib import Path

from fasthtml.common import FastHTML
from htpy import a, body, head, html, link, table, td, th, title, tr
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse, Response

from utils import LABELS, HEADERS, KEYS, fmt

LESSON_DIR = Path(__file__).parent
DB_PATH = LESSON_DIR / "sightings.db"


def make_app(db_path=DB_PATH):
    app = FastHTML()

    @app.get("/")
    async def index():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("select * from sightings").fetchall()
        conn.close()
        return HTMLResponse(str(
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
        ))

    @app.get("/sighting/{sighting_id:int}")
    async def detail(sighting_id: int):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "select * from sightings where id = ?", [sighting_id]
        ).fetchone()
        conn.close()
        if row is None:
            raise HTTPException(status_code=404, detail=f"No sighting with ID {sighting_id}")
        return HTMLResponse(str(
            html(lang="en")[
                head[
                    title[f"Sighting {sighting_id}"],
                    link(rel="stylesheet", href="/style.css"),
                ],
                body[
                    table[
                        [
                            tr[
                                td(class_="label")[label],
                                td[fmt(row[key])],
                            ]
                            for key, label in LABELS.items()
                        ],
                    ],
                    a(href="/")["Back to all sightings"],
                ],
            ]
        ))

    @app.get("/style.css")
    def styles():
        return Response((LESSON_DIR / "style.css").read_text(), media_type="text/css")

    return app


app = make_app()
