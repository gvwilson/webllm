# 2026-05-11 Playwright Lesson

## Task

Add a lesson on browser testing with Playwright. Directory slug: `testclient`.

## Actions

-   Created `testclient/` directory with all lesson files.
-   `server_pw.py`: copied from `forms/server_upload.py`; changed `DB_PATH` to read from
    `SASQUATCH_DB` environment variable so tests can point at a throwaway database.
-   `conftest.py`: session-scoped `server_url` fixture that copies the production database,
    sets `SASQUATCH_DB`, starts the server with `subprocess.Popen`, and tears it down afterward.
-   `test_browser.py`: four tests covering page title, table presence, link clicking, and form fill.
-   Added `testclient` to lesson list in `README.md` between forms and finale.
-   Added `playwright2025` to `bibliography/index.md`.
-   Added `end-to-end-test`, `headless`, and `locator` to `glossary/index.md`.
-   Added `[playwright-python]` to `_extras/links.md`.
