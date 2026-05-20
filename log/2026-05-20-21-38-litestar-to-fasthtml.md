# Replace Litestar with FastHTML

## Prompt

Replace litestar with fasthtml everywhere, updating examples and prose.

## Actions

Replaced Litestar with FastHTML (package `python-fasthtml`) throughout the project.
Added `uvicorn` as an explicit dependency since it is the ASGI server used to run FastHTML apps.

### Key API translations

| Litestar | FastHTML / Starlette |
|---|---|
| `from litestar import Litestar, get, post, MediaType` | `from fasthtml.common import FastHTML` |
| `@get("/", media_type=MediaType.HTML)` | `@app.get("/")` returning `HTMLResponse(...)` |
| `Litestar([handler, ...])` | `app = FastHTML()` + `@app.get/post` decorators |
| `raise NotFoundException(...)` | `raise HTTPException(status_code=404, ...)` |
| `Redirect("/", status_code=303)` | `RedirectResponse("/", status_code=303)` |
| `Body(media_type=RequestEncodingType.URL_ENCODED)` | `await request.form()` |
| `CsvUpload` dataclass + `UploadFile` | `await request.form()` then `.get("csv_file").read()` |
| `from litestar.testing import TestClient` | `from starlette.testclient import TestClient` |
| `litestar run --app module:app` | `uvicorn module:app --reload` |
| `litestar run --ssl-certfile ... --app ...` | `uvicorn module:app --ssl-certfile ...` |

### Structural change in forms/server_add.py

Routes were defined at module level and injected via Litestar's `Provide` dependency system.
Restructured to define routes as closures inside `make_app`, matching the pattern used everywhere else.

### Files modified (28 total)

Config/metadata: `pyproject.toml`, `CLAUDE.md`, `_extras/links.md`, `bibliography/index.md`, `glossary/index.md`

Server Python: `server/server_hello.py`, `server/server_table.py`, `server/server_detail.py`,
`database/server_db.py`, `testserver/server_testable.py`, `testdatabase/server_db.py`,
`forms/server_delete.py`, `forms/server_add.py`, `forms/server_upload.py`,
`dynamic/server_scroll.py`, `dynamic/server_detail.py`, `logging/server_stream.py`,
`logging/server_rotate.py`, `testclient/server_pw.py`

Test Python: `testserver/test_server_status.py`, `testserver/test_server_data.py`,
`testdatabase/test_detail.py`, `testdatabase/test_index.py`, `database/test_server_db.py`,
`forms/test_server_forms.py`, `testclient/conftest.py`

Shell scripts: `server/run1.sh`, `server/run2.sh`, `server/run3.sh`, `database/run.sh`,
`forms/run.sh`, `dynamic/run.sh`, `logging/run.sh`, `secure/run_secure.sh`

Markdown lessons: `server/index.md`, `testserver/index.md`, `testclient/index.md`,
`forms/index.md`, `secure/index.md`
