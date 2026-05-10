# Testing the Server

**Date:** 2026-05-10 19:57 UTC

## Prompts

-   User asked: what is the best way for this audience to test the server?

## Context

-   Current lesson: `server/` — Litestar server with three files (server1.py, server2.py, server3.py)
-   Stack: Litestar, htpy, uv, pytest, Playwright
-   Audience: undergrad researchers, one semester Python, nervous about tooling

## Discussion

Decided on `TestClient` (not Playwright) for this lesson.
Save Playwright for when Alpine.js or HTMX interactions first require a real browser.

## Actions Taken

-   Added `## Style Rules` to `CLAUDE.md` with no-horizontal-rule rule
-   Added `testserver` lesson to `README.md` between `server` and `finale`
-   Added `pytest` and `httpx` to `pyproject.toml` dependencies
-   Added `[pytest]` link to `_extras/links.md`
-   Added `pytest2025` to `bibliography/index.md`
-   Added glossary entries: `fixture`, `status-code`, `test-client`
-   Created `testserver/conftest.py` (sys.path setup for server imports)
-   Created `testserver/test_server1.py` (4 tests against SIGHTINGS)
-   Created `testserver/test_server2.py` (3 tests with controlled SMALL data using monkeypatch)
-   Created `testserver/run_tests.sh`
-   Created `testserver/index.md` (full lesson)
