# Logging

## Goals

-   Understand why structured logging is more useful than `print` statements.
-   Use Python's built-in `logging` module to create a named logger for a module.
-   Call a `configure_logging` function to set the active level and route messages to the terminal.
-   Add a file handler so that log records survive after the server stops.
-   Catch exceptions with `logger.exception` to record a full traceback when something goes wrong.

## Why Not Just Print?

> What is wrong with using `print` to debug an application?

-   Every `print` call runs unconditionally, whether you want its output or not
-   When you are done debugging, you have to find and remove each one by hand
    -   Missing even one leaves stray output in every response forever
-   All `print` output looks the same: there is no way to tell a routine status message from a serious error
-   A server handling dozens of requests per minute produces a wall of text that is hard to read

> What does Python's `logging` module give you that `print` does not?

-   Every message has a [%g log-level "log level" %]: `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`,
    in increasing order of severity
    -   One setting silences everything below a chosen level without touching the code:
        switching from `DEBUG` to `INFO` hides all the verbose diagnostic messages at once
-   Every message is stamped automatically with the time, the level, and the name of the source that produced it
-   A [%g logger "logger" %] is created once per module with `logging.getLogger(__name__)`
    -   `__name__` is Python's built-in name for the current module, so each logger is named after its file
    -   Separate names make it easy to trace a message back to its source when reading the log later
-   Log messages go to one or more [%g log-handler "log handlers" %]
    that decide where the output actually lands
    -   Terminal, file, database, or monitoring service

## Adding a Logger to the Server

> Add logging to `server_stream.py` so that the server records what it is doing.
> Add a `configure_logging` function that can be called once at startup.

-   `logger = logging.getLogger(__name__)` goes below the imports and above the first function,
    at module level so every handler in the file shares the same logger
-   `configure_logging` calls `logging.basicConfig`, which sets up the root logger:
    -   `level=logging.DEBUG` shows every message; raise it to `logging.INFO` in production
        to silence diagnostic chatter without changing any handler code
    -   `format="%(asctime)s %(levelname)-8s %(name)s %(message)s"` stamps each line with
        the time, the level (padded to eight characters so columns stay aligned),
        the logger name, and the message
    -   `handlers=[logging.StreamHandler()]` sends output to the terminal
-   Nothing appears in the log until `configure_logging()` is called; this is a common first-time surprise
-   Calling `configure_logging()` at module level, before `app = make_app()`, means logging is
    ready before any request arrives

> Add log calls to the handlers. Use `INFO` when a sighting is inserted or deleted,
> `WARNING` when an optional field is left blank, and `DEBUG` when a detail page loads successfully.

-   `logger.info("home page: %d sightings", len(rows))` records the count each time the index loads

<div class="callout" markdown="1">

### Pass Values as Arguments, Not f-Strings

Write `logger.info("count: %d", n)` rather than `logger.info(f"count: {n}")`.
The `logging` module skips string formatting entirely when the message level is below the active threshold,
so the f-string approach does unnecessary work on every call even when the output is never shown.

</div>

-   `logger.warning("new sighting added without weight")` flags incomplete submissions without crashing
-   `logger.debug("sighting %d retrieved", sighting_id)` disappears automatically when the level is
    raised to `INFO`, so it costs nothing in production
-   `logger.warning("sighting %d not found", sighting_id)` before raising `NotFoundException`
    records every 404 before the framework handles it

[%inc server_stream.py mark=logging-setup %]

[%inc server_stream.py mark=detail-handler %]

[%inc server_stream.py mark=add-handler %]

Start the server from the `logging/` directory:

[%inc run.sh %]

Open the app in a browser and add a sighting with the weight field blank.
The terminal shows timestamped lines like these:

[%inc sample.log %]

## Writing Logs to a File

> Copy `server_stream.py` to `server_rotate.py`
> and update `configure_logging` to also write to a file alongside the terminal output.

-   `LOG_PATH = LESSON_DIR / "sightings.log"` puts the file next to the server code
-   `logging.FileHandler(LOG_PATH)` opens the file and writes each message to it
-   A single logger can have any number of handlers:
    if both a `StreamHandler` and a `FileHandler` are given to `basicConfig`
    then each message goes to both destinations
-   Log files should not be committed to version control
    -   Add `*.log` to `.gitignore` so the file never ends up in a repository by accident

> What happens if the log file grows too large, and how do you handle it?

-   A server running for months can produce a log file large enough to fill the disk
-   `logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=1_000_000, backupCount=3)`
    creates a file that resets instead of growing without limit
    -   When the file reaches `maxBytes` bytes (here, one megabyte), the handler renames it
        `sightings.log.1` and starts a fresh `sightings.log`
    -   Old backups beyond `backupCount` are deleted automatically,
        so the total disk use never exceeds four megabytes regardless of how long the server runs
-   `logging.handlers` is a submodule that must be imported explicitly with
    `import logging.handlers`; it is not available through `import logging` alone

## Catching Exceptions in the Log

> Modify the CSV upload handler in `server_rotate.py` to catch exceptions and record the full
> traceback instead of crashing and returning a 500 response.

-   Without a try/except, a malformed CSV row terminates the handler immediately and returns a
    blank 500 error; the log shows nothing useful
-   Wrapping each row insert in `try` / `except Exception` catches any error that might arise:
    a missing column, a value that cannot be converted to a float, a database constraint violation
-   After the except block, the loop continues with the next row rather than aborting the upload
-   `logger.exception("failed to insert row: %s", dict(row))` logs the message and then appends
    the full traceback automatically
    -   `exception` is shorthand for `error` combined with `traceback.format_exc()`;
        using `logger.error` alone would log the message but lose the traceback

> What does the log file contain after a CSV upload whose column names do not match what the
> handler expects?

-   The Python dictionary lookup `row["species"]` raises `KeyError` if the CSV header is
    `Species` (capital S) instead of `species`
-   The log entry looks like this:

```
2026-05-11 10:34:22,019 ERROR    server_rotate failed to insert row: {'Species': 'G. canadensis', ...}
Traceback (most recent call last):
  File "server_rotate.py", line 140, in upload_csv
    row["species"],
KeyError: 'species'
```

-   The timestamp, level, and module name appear on the first line; the traceback follows immediately
-   The log file now contains a permanent record of the failure even after the server restarts,
    which makes it possible to diagnose problems that happened hours ago

[%inc server_rotate.py mark=configure-logging %]

[%inc server_rotate.py mark=upload-csv %]

See [%b python-logging2025 %] for the full Python logging documentation.

## Check Understanding

<details markdown="1">
<summary markdown="1">A classmate adds `logger.debug("starting upload")` to the upload handler but sees nothing in the terminal. What are the two most likely causes?</summary>

Either `configure_logging` was never called, so no handler is attached to the root logger,
or `configure_logging` was called with `level=logging.INFO`, which silences `DEBUG` messages.
Both produce the same symptom: complete silence.

</details>

<details markdown="1">
<summary markdown="1">Two modules each call `logging.getLogger("sightings")` instead of `logging.getLogger(__name__)`. When reading the log, how can you tell which module produced a given message?</summary>

You cannot.
Both loggers share the same name, so every message shows `"sightings"` as the source
regardless of which file it came from.
Using `logging.getLogger(__name__)` in each module gives each logger a distinct name
matching its filename, making every message traceable to its origin.

</details>

<details markdown="1">
<summary markdown="1">Why is `logger.warning` the right level when a sighting is submitted without a weight, rather than `logger.info` or `logger.error`?</summary>

`INFO` is for routine events during normal operation.
`ERROR` is for failures that prevent the operation from completing.
A missing optional weight is neither: the sighting was inserted successfully,
but the data is incomplete in a way worth noticing.
`WARNING` communicates "something unusual happened, but the application is still working."

</details>

<details markdown="1">
<summary markdown="1">After three weeks, the `sightings.log` file is four gigabytes and the disk is full. What one change to `configure_logging` prevents this from recurring?</summary>

Replace `FileHandler` with `logging.handlers.RotatingFileHandler` and set `maxBytes` and `backupCount`.
The handler then caps the file at `maxBytes` bytes and keeps at most `backupCount` old copies,
so total disk use stays bounded regardless of how long the server runs.

</details>

<details markdown="1">
<summary markdown="1">The code below is meant to log a failure, but the traceback never appears in the log file. What is wrong?</summary>

`logger.error` logs the message but discards the traceback.
Replace it with `logger.exception("upload failed: %s", e)`,
which automatically appends the current exception's full traceback to the log entry.

</details>

```python
except Exception as e:
    logger.error("upload failed: %s", e)
```

## Exercises

### Log Elapsed Time

Add timing to the `detail` handler.
Use `time.perf_counter()` before and after the database query to measure elapsed time in milliseconds,
and log it at the `DEBUG` level: `"sighting %d retrieved in %.1f ms"`.

### Filter Levels to Separate Files

Configure `configure_logging` with two `RotatingFileHandler` instances: one that records only
`WARNING` and above to `errors.log`, and one that records everything to `all.log`.
To restrict a handler to a minimum level, call `handler.setLevel(logging.WARNING)` before passing
it into `basicConfig`.
Submit the add form once with weight left blank and confirm the warning appears in both files.

### Log Events to the Database

Add a table called `event_log` to the sightings database with columns for the timestamp,
level name, logger name, and message.
Ask an LLM to generate a logging handler that inserts each log record into this table as a row,
then add the handler to `configure_logging` alongside the existing file handler.
Start the server, load a few pages, and confirm the handler is working by running
`select * from event_log limit 5` in the SQLite shell.

### Test That Warnings Are Emitted

Write a pytest test that submits the add form with weight left blank
and confirms that a warning was recorded.
pytest's `caplog` fixture captures log records during a test without writing to a file:

```python
def test_missing_weight_logged(caplog, small_db):
    with caplog.at_level(logging.WARNING):
        # submit form and check records
        assert any("without weight" in r.message for r in caplog.records)
```

Reuse the `small_db` fixture from the `testdatabase` lesson to give the test a fresh database.
