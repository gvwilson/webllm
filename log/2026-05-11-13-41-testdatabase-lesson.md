# 2026-05-11 13:41 — Add testdatabase lesson

## Task

Add a new lesson `testdatabase` between `database` and `forms` that introduces
`conftest.py` for sharing fixtures across multiple test files.

## Files Created

-   `testdatabase/index.md` — lesson content
-   `testdatabase/conftest.py` — shared `small_db` fixture (extracted from database lesson)
-   `testdatabase/test_index.py` — tests for the index route
-   `testdatabase/test_detail.py` — tests for the detail route
-   `testdatabase/run_tests.sh` — command to run the tests
-   `testdatabase/server_db.py` — copy of `database/server_db.py` for self-containedness
-   `testdatabase/style.css` — copy of `database/style.css`

## Files Modified

-   `README.md` — added `testdatabase` between `database` and `forms` in the lessons list
-   `glossary/index.md` — added `conftest-file` and `fixture` entries

## Rationale

The `testclient` lesson uses a `conftest.py` with a session-scoped subprocess fixture,
which is complex. Without prior exposure to `conftest.py`, learners would encounter
the concept in a high-cognitive-load context. This lesson introduces `conftest.py` in a
simpler setting (function-scoped, in-memory database) so the idea is familiar before
it reappears with more moving parts.
