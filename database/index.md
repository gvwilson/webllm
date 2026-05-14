# Using a Database

## Goals

-   Understand why a database is more useful than a Python list for storing application data.
-   Use Python's built-in `sqlite3` module to create a database and populate it with data.
-   Write SQL queries to retrieve all rows from a table and to look up a single row by ID.
-   Rewrite the server to read sightings from a database file instead of an in-memory list.
-   Use a temporary database in tests so that tests do not depend on production data.

## Why Not a List?

*What are the problems with storing the sightings data in a Python list?*

-   Every time the server restarts, the list is re-created from the source code
    -   Any records added while the server was running are lost
-   If two people run the server on different machines, they each have their own private copy of the data
    -   A sighting added on one machine is invisible to everyone else
-   Searching through a list means reading every item in order
    -   For twenty sightings this is fast; for two million it is not

*What is a database and why is SQLite a good choice for this application?*

-   A [%g database "database" %] stores data in a way that survives program restarts
-   A [%g sql "SQL" %] database organizes data into [%g db-table "tables" %],
    where each table has named [%g column "columns" %] and zero or more [%g row "rows" %]
-   [SQLite][sqlite] stores an entire database in a single file on disk,
    which is easy to back up, share, and version-control
-   Python includes the `sqlite3` module in its standard library, so no extra packages are needed

## Creating a Database

*Write a Python script called `create_db.py` that uses `sqlite3` to create a file called
`sightings.db` with one table named `sightings`.
The table should be populated with the data from `dataset.py`.*

-   `sqlite3.connect(path)` opens the database at `path`, creating the file if it does not exist
-   `conn.execute(sql)` runs a [%g query "query" %] against the open database
-   `create table if not exists sightings (...)` defines the shape of the table:
    -   `integer primary key` marks `id` as the unique identifier for each row
    -   `text not null` means the column must contain a value; `text` alone allows [%g db-null "null" %]
    -   `real` stores a floating-point number, matching Python's `float`
-   `conn.commit()` saves all the changes to disk; without it the writes are discarded when the
    connection closes
-   `conn.close()` releases the file so other programs can access it

[%inc create_db.py omit=skip %]

Run the script once to create the database:

[%inc create_db.sh %]

## A Database-Backed Server

*Rewrite `server_testable.py` as `server_db.py` so that `make_app` takes a database path instead of a
list of sightings.
The index route should read all rows from the database, and the detail route should look up
one row by ID.*

-   `sqlite3.connect(db_path)` opens the database; `conn.close()` releases it when done
-   Setting `conn.row_factory = sqlite3.Row` makes each result row behave like a dictionary,
    so `row["species"]` works the same way `s["species"]` did with the list
-   `conn.execute("select * from sightings").fetchall()` retrieves every row in the table
    -   `select *` means "return all columns"
    -   `from sightings` names the table to read from
    -   `fetchall()` collects the results into a Python list
-   `conn.execute("select * from sightings where id = ?", [sighting_id]).fetchone()` retrieves one row
    -   `where id = ?` filters the results to rows where `id` matches the given value
    -   The `?` is a [%g placeholder "placeholder" %]: `sqlite3` fills it in safely,
        preventing a common security mistake called [%g sql_injection "SQL injection" %]
    -   `fetchone()` returns the first matching row, or `None` if no row matched
-   `if row is None: raise NotFoundException(...)` works exactly as before,
    because `fetchone()` returns `None` for a missing ID just as the old loop did

<div class="callout" markdown="1">

### SQL Injection

If you built the query with an f-string,
like `f"select * from sightings where id = {sighting_id}"`,
a user could visit a URL like `/sighting/1 or 1=1`, which would make the query read
`select * from sightings where id = 1 or 1=1`.
Because `1=1` is always true, this returns every row in the table instead of just one.
With a destructive statement the damage is worse: `1; drop table sightings` would delete all
the data.
The `?` placeholder prevents this by telling `sqlite3` to treat the value as data,
never as SQL.

</div>

[%inc server_db.py mark=db-index %]

[%inc server_db.py mark=db-detail %]

Start the server the same way as before (after running `create_db.py` first):

[%inc run.sh %]

## Testing with a Temporary Database

*Write a test file called `test_server_db.py` that uses pytest's `tmp_path` fixture to create
a small temporary database for each test, and uses `make_app` with that database path to
test the index, detail, and 404 routes.*

-   pytest's built-in `tmp_path` fixture provides a fresh temporary directory for each test
    -   The directory and everything in it is automatically deleted when the test finishes
-   A `@pytest.fixture` named `small_db` creates a two-row database in `tmp_path` and returns its path
    -   Each test that lists `small_db` as a parameter receives a fresh database
    -   Tests are completely isolated: one test's writes cannot affect another's
-   `make_app(small_db)` creates a server that reads from the temporary database,
    not from `sightings.db`
    -   Tests no longer break if someone adds rows to the production database

[%inc test_server_db.py %]

Run the tests from the `database/` directory:

[%inc run_tests.sh %]

## Check Understanding

<details markdown="1">
<summary markdown="1">What happens if you call `conn.execute(...)` several times but never call `conn.commit()`?</summary>

The changes are held in memory but never written to disk.
When `conn.close()` is called, all of them are discarded.
The database file on disk remains unchanged, as if the `execute` calls never happened.

</details>

<details markdown="1">
<summary markdown="1">The code below always prints zero rows, even though `sightings.db` has twenty rows. What is wrong?</summary>

```python
conn = sqlite3.connect("sightings.db")
conn.execute("insert into sightings values (?, ?, ?, ?, ?, ?, ?, ?)", [21, "G. canadensis", None, 160, "brown", "2024-08-01 10:00", 50.0, -120.0])
rows = conn.execute("select * from sightings").fetchall()
print(len(rows))
conn.close()
```

`conn.commit()` is missing after the `insert`.
Without it, the insert is not saved to disk, so the `select` that follows still sees the
original twenty rows---and once `conn.close()` is called, the insert is discarded entirely.
Add `conn.commit()` between the `execute` and the `select`.

</details>

<details markdown="1">
<summary markdown="1">What does `fetchone()` return when no row matches the `where` clause?</summary>

It returns `None`.
This is why `server_db.py` checks `if row is None` before trying to read values from the row:
accessing a column on `None` would raise an `AttributeError`.

</details>

See [%b sqlite2025 %] for the SQLite documentation and [%b python-sqlite2025 %]
for the Python `sqlite3` module reference.

## Exercises

### Count the Rows

After calling `create_db`, open `sightings.db` in a Python script and print the number of
rows in the `sightings` table.
Look up the SQL function `count(*)` to do this in a single query.

### Check for Duplicates

Modify `create_db.py` so that running it twice does not add duplicate rows.
The `create table if not exists` clause already handles the table; think about how to handle
the `insert` statements.

### Filter by Species in the Tests

Add a test to `test_server_db.py` that visits the index page and confirms that both
`"G. canadensis"` and `"G. horribilus"` appear in the response when `SMALL` contains one
row of each.

### Inspect the Database Directly

SQLite databases can be opened and queried from the command line.
Run `sqlite3 sightings.db` and use the `.tables` command to list tables, then run
`select count(*) from sightings;` to confirm the row count.
Exit with `.quit`.
