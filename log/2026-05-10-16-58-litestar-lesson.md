# Litestar Lesson

**Created:** 2026-05-10 16:58 UTC

## Task

Create a lesson showing how to use Litestar to serve data. The lesson
builds from a route that serves a static message to one that generates
a page with a single table to one where sighting IDs are links to
detail pages. Uses a simple external CSS file. No automated tests yet.

## Files Created

-   `litestar/dataset.py` — 20-row synthetic sightings data
-   `litestar/style.css` — simple external stylesheet
-   `litestar/server1.py` — one route, plain-text response
-   `litestar/server2.py` — HTML table route + CSS route
-   `litestar/server3.py` — adds detail route with two-column table
-   `litestar/run1.sh`, `run2.sh`, `run3.sh` — shell commands
-   `litestar/index.md` — lesson

## Files Modified

-   `README.md` — added lesson to lesson list
-   `glossary/index.md` — added web server, route, port, localhost,
    path parameter, media type
-   `bibliography/index.md` — added Litestar entry
-   `_extras/links.md` — added `[litestar]` link
-   `pyproject.toml` — added `litestar>=2.0.0` dependency
