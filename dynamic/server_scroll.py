import sqlite3
from pathlib import Path

from fasthtml.common import FastHTML
from htpy import body, div, h1, head, html, link, script, table, tbody, td, th, thead, title, tr
from starlette.responses import HTMLResponse, Response

from utils import HEADERS, KEYS, fmt

LESSON_DIR = Path(__file__).parent
DB_PATH = LESSON_DIR.parent / "database" / "sightings.db"

# Number of rows fetched from the database in each request.
PAGE_SIZE = 20

# mccole:helpers
def make_row(row):
    return tr[
        td[str(row["id"])],
        [td[fmt(row[k])] for k in KEYS[1:]],
    ]


def make_sentinel(offset):
    """Return a table row that triggers the next page load when scrolled into view."""
    return tr(
        hx_get=f"/rows?offset={offset}",
        hx_trigger="revealed",
        hx_swap="outerHTML",
    )[td(colspan=len(HEADERS))["Loading..."]]
# mccole:/helpers


# mccole:index-route
def make_app(db_path=DB_PATH):
    app = FastHTML()

    @app.get("/")
    async def index():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "select * from sightings limit ?", [PAGE_SIZE]
        ).fetchall()
        conn.close()
        return HTMLResponse(str(
            html(lang="en")[
                head[
                    title["Sasquatch Sightings"],
                    link(rel="stylesheet", href="/style.css"),
                    script(src="https://unpkg.com/htmx.org@2.0.4"),
                ],
                body[
                    h1["Sasquatch Sightings"],
                    div(class_="scroll-container")[
                        table[
                            thead[tr[[th[col] for col in HEADERS]]],
                            tbody[
                                [make_row(row) for row in rows],
                                make_sentinel(PAGE_SIZE) if len(rows) == PAGE_SIZE else "",
                            ],
                        ],
                    ],
                ],
            ]
        ))
# mccole:/index-route

# mccole:more-rows
    @app.get("/rows")
    async def more_rows(offset: int = 0):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "select * from sightings limit ? offset ?", [PAGE_SIZE, offset]
        ).fetchall()
        conn.close()
        result = "".join(str(make_row(row)) for row in rows)
        if len(rows) == PAGE_SIZE:
            result += str(make_sentinel(offset + PAGE_SIZE))
        return HTMLResponse(result)

    @app.get("/style.css")
    def styles():
        return Response((LESSON_DIR / "style.css").read_text(), media_type="text/css")

    return app


app = make_app()
# mccole:/more-rows
