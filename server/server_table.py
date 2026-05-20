from pathlib import Path

from fasthtml.common import FastHTML
from htpy import body, head, html, link, table, td, th, title, tr
from starlette.responses import HTMLResponse, Response

from dataset import SIGHTINGS
from utils import HEADERS, KEYS, fmt

LESSON_DIR = Path(__file__).parent
app = FastHTML()


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
                    [tr[[td[fmt(s[k])] for k in KEYS]] for s in SIGHTINGS],
                ],
            ],
        ]
    ))


@app.get("/style.css")
def styles():
    return Response((LESSON_DIR / "style.css").read_text(), media_type="text/css")
