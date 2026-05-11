from pathlib import Path

from htpy import a, body, head, html, link, table, td, th, title, tr
from litestar import Litestar, MediaType, get
from litestar.exceptions import NotFoundException

from dataset import SIGHTINGS

LESSON_DIR = Path(__file__).parent

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
                        tr[
                            td[a(href=f"/sighting/{s['id']}")[str(s["id"])]],
                            [td[fmt(s[k])] for k in KEYS[1:]],
                        ]
                        for s in SIGHTINGS
                    ],
                ],
            ],
        ]
    )


@get("/sighting/{sighting_id:int}", media_type=MediaType.HTML)
async def detail(sighting_id: int) -> str:
    for s in SIGHTINGS:
        if s["id"] == sighting_id:
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
                                    td(class_="label")[label],
                                    td[fmt(s[key])],
                                ]
                                for key, label in LABELS.items()
                            ],
                        ],
                        a(href="/")["Back to all sightings"],
                    ],
                ]
            )
    raise NotFoundException(f"No sighting with ID {sighting_id}")


@get("/style.css", media_type="text/css")
async def styles() -> str:
    return (LESSON_DIR / "style.css").read_text()


app = Litestar([index, detail, styles])
