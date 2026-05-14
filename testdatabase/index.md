# Testing with Fixtures

## Goals

-   Understand why putting a fixture in one test file makes it unavailable to other test files.
-   Use `conftest.py` to define fixtures that pytest shares automatically across all test files in a directory.
-   Split tests into multiple files, each focused on one part of the application.

## The Duplication Problem

> The previous lesson put `small_db` directly in `test_server_db.py`.
> What happens if you want to write a second test file that also needs a small database?

-   A [%g fixture "fixture" %] defined inside a test file is private to that file
    -   Importing it from another test file would work, but it breaks pytest's fixture discovery
    -   Copying the fixture into every new test file means maintaining the same setup code in multiple places
    -   If the database schema changes, every copy has to be updated separately
-   The fixture is doing real work: creating a temporary database, inserting rows, and returning a path
    -   That work belongs in one place, shared by all the tests that need it

> Where does pytest look when it needs a fixture that is not defined in the current test file?

-   pytest looks for a file named [%g conftest-file "`conftest.py`" %] in the same directory as the test file,
    then in each parent directory up to the project root
    -   No import statement is required: fixtures defined in `conftest.py` are available to every test file
        in the same directory and all subdirectories
    -   pytest finds `conftest.py` by convention, not by any explicit reference in the test files

## Extracting the Fixture

> Move the `SMALL` list, the SQL constants, and the `small_db` fixture from `test_server_db.py`
> into a new file called `conftest.py` in the same directory.

-   Everything the fixture needs moves with it: `SMALL`, `CREATE_TABLE`, and `INSERT_ROW`
    -   Test files that use `small_db` do not import anything from `conftest.py`;
        pytest injects the fixture automatically based on the parameter name
-   The fixture itself is unchanged: it still uses `tmp_path` to get a fresh directory,
    creates the database, inserts the two rows, and returns the path

[%inc conftest.py %]

## Testing in Separate Files

> Write a file called `test_index.py` with tests that check the index route,
> and a file called `test_detail.py` with tests that check the detail route.
> Both files should use `small_db`.

-   `test_index.py` imports only `TestClient` and `make_app`
    -   `small_db` arrives as a parameter
    -   `test_index_ok` checks that the home page responds with 200 and contains the site title
    -   `test_index_shows_both_species` confirms both species from `SMALL` appear in the page
-   `test_detail.py` also imports only `TestClient` and `make_app`
    -   `test_detail_ok` visits sighting 1 and confirms the species name appears
    -   `test_missing_sighting` confirms that a nonexistent ID returns 404
    -   `test_none_displayed_as_empty` confirms that a sighting with null fields
        does not show the word `"None"` in the page

[%inc test_index.py %]

[%inc test_detail.py %]

-   Run both files together from the `testdatabase/` directory:

[%inc run_tests.sh %]

-   pytest loads `conftest.py` once and makes `small_db` available to every test in both files
-   Each test that lists `small_db` as a parameter gets its own fresh database,
    so a write in one test cannot affect another

## Check Understanding

See [%b pytest2025 %] for the full pytest documentation,
including the reference page on fixtures and `conftest.py`.

<details markdown="1">
<summary markdown="1">The code below causes an error even though `small_db` is defined in `conftest.py`. What is wrong?</summary>

pytest injects fixtures automatically by matching parameter names.
Importing a fixture function and passing it as a parameter bypasses that mechanism.
pytest no longer recognizes it as a fixture and raises an error.
Remove the import line and let pytest inject `small_db` on its own.

</details>

```python
from conftest import small_db

def test_index_ok(small_db):
    ...
```

<details markdown="1">
<summary markdown="1">Each test that uses `small_db` gets its own database. What would happen if they all shared one database instead?</summary>

Tests that add or delete rows would affect every test that runs afterward.
The order in which pytest runs tests would determine whether they pass or fail,
which makes failures hard to reproduce and debug.
Keeping each test isolated means it can be run alone or in any order and still produce the same result.

</details>

<details markdown="1">
<summary markdown="1">The test below always passes, even when it should not. What is wrong?</summary>

`status_code != 200` passes for any code other than 200, including 500 (server error).
A bug that causes the server to crash would make this test pass when it should fail.
The assertion should be `assert response.status_code == 404` to confirm the right kind of failure.

</details>

```python
def test_missing_sighting(small_db):
    with TestClient(app=make_app(small_db)) as client:
        response = client.get("/sighting/9999")
    assert response.status_code != 200
```

## Exercises

### Add a Test for the CSS Route

Add a test to `test_index.py` that sends `GET /style.css`.
It must check that the response status code is 200 and that the response text contains `"table"`.

### Test a Specific Detail

Add a test to `test_detail.py` that visits `/sighting/2`
and confirms that `"G. horribilus"` appears in the response.

### Add a Third Test File

Create `test_links.py` that uses `small_db` to check that
the index page contains two links inside the table
and that the detail page for sighting 1 contains a link whose text is `"Back to all sightings"`.
You will need to look for the right strings in `response.text`.

### Change the Test Data

Add a third row to `SMALL` in `conftest.py` with a species of `"G. canadensis"` and a different color.
Without changing any test assertions, run the suite and confirm that all tests still pass,
then explain why `test_index_shows_both_species` still passes even though the number of rows changed.

### Confirm Isolation

Add a test to `test_detail.py` that inserts a third row directly into `small_db` using `sqlite3`,
then checks that the index page shows three links.
Run the full suite and confirm that `test_index_ok` still passes with only two links,
which shows that each test received its own database.
