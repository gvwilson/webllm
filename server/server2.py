from pathlib import Path

from htpy import body, head, html, link, table, td, th, title, tr
from litestar import Litestar, MediaType, get

from dataset import SIGHTINGS

LESSON_DIR = Path(__file__).parent

HEADERS = ["ID", "Species", "Sex", "Weight (kg)", "Color", "Date/Time", "Latitude", "Longitude"]
KEYS = ["id", "species", "sex", "weight", "color", "datetime", "latitude", "longitude"]


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
                    [
                        tr[[td[str(s[k]) if s[k] is not None else ""] for k in KEYS]]
                        for s in SIGHTINGS
                    ],
                ],
            ],
        ]
    )


@get("/style.css", media_type="text/css")
async def styles() -> str:
    return (LESSON_DIR / "style.css").read_text()


app = Litestar([index, styles])
