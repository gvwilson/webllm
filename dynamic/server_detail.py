import sqlite3
from pathlib import Path

from fasthtml.common import FastHTML
from htpy import body, div, h1, head, html, link, p, script, table, tbody, td, th, thead, title, tr
from starlette.responses import HTMLResponse, Response

from utils import HEADERS, KEYS, LABELS, fmt

LESSON_DIR = Path(__file__).parent
DB_PATH = LESSON_DIR.parent / "database" / "sightings.db"

# Number of rows fetched from the database in each request.
PAGE_SIZE = 20


# mccole:make-row
def make_row(row):
    return tr(
        hx_get=f"/sighting/{row['id']}/detail",
        hx_target="#detail",
        hx_swap="innerHTML",
    )[
        td[str(row["id"])],
        [td[fmt(row[k])] for k in KEYS[1:]],
    ]
# mccole:/make-row


def make_sentinel(offset):
    """Return a table row that triggers the next page load when scrolled into view."""
    return tr(
        hx_get=f"/rows?offset={offset}",
        hx_trigger="revealed",
        hx_swap="outerHTML",
    )[td(colspan=len(HEADERS))["Loading..."]]


# mccole:index
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
                    div(id="detail", class_="detail-pane")[
                        p["Click any row to see the full record."]
                    ],
                ],
            ]
        ))
# mccole:/index

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

# mccole:detail-fragment
    @app.get("/sighting/{sighting_id:int}/detail")
    async def detail_fragment(sighting_id: int):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "select * from sightings where id = ?", [sighting_id]
        ).fetchone()
        conn.close()
        if row is None:
            return HTMLResponse("<p>Sighting not found.</p>")
        return HTMLResponse(str(
            table[
                [
                    tr[
                        td(class_="label")[lbl],
                        td[fmt(row[key])],
                    ]
                    for key, lbl in LABELS.items()
                ]
            ]
        ))

    @app.get("/style.css")
    def styles():
        return Response((LESSON_DIR / "style.css").read_text(), media_type="text/css")

    return app


app = make_app()
# mccole:/detail-fragment
