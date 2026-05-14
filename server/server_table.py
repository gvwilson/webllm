from pathlib import Path

from htpy import body, head, html, link, table, td, th, title, tr
from litestar import Litestar, MediaType, get

from dataset import SIGHTINGS
from utils import HEADERS, KEYS, fmt

LESSON_DIR = Path(__file__).parent


@get("/", media_type=MediaType.HTML)
async def index() -> str:
    return str(
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
    )


@get("/style.css", media_type="text/css")
async def styles() -> str:
    return (LESSON_DIR / "style.css").read_text()


app = Litestar([index, styles])
