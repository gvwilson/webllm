from pathlib import Path

from fasthtml.common import FastHTML
from htpy import a, body, head, html, link, table, td, th, title, tr
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse, Response

from dataset import SIGHTINGS
from utils import HEADERS, KEYS, LABELS, fmt

LESSON_DIR = Path(__file__).parent
app = FastHTML()


# mccole:index-with-links
@app.get("/")
async def index():
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
                            td[a(href=f"/sighting/{s['id']}")[str(s["id"])]],
                            [td[fmt(s[k])] for k in KEYS[1:]],
                        ]
                        for s in SIGHTINGS
                    ],
                ],
            ],
        ]
    ))
# mccole:/index-with-links


# mccole:detail-route
@app.get("/sighting/{sighting_id:int}")
async def detail(sighting_id: int):
    for s in SIGHTINGS:
        if s["id"] == sighting_id:
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
                                    td[fmt(s[key])],
                                ]
                                for key, label in LABELS.items()
                            ],
                        ],
                        a(href="/")["Back to all sightings"],
                    ],
                ]
            ))
    raise HTTPException(status_code=404, detail=f"No sighting with ID {sighting_id}")


@app.get("/style.css")
def styles():
    return Response((LESSON_DIR / "style.css").read_text(), media_type="text/css")
# mccole:/detail-route
