# Testing the Server

## Goals

-   Understand why running automated tests is faster and more reliable than manually checking routes in a browser.
-   Use Litestar's test client to send HTTP requests to the application without starting a real server.
-   Write tests against the application's existing data to check status codes and page content.
-   Refactor the server to accept a dataset as a parameter so tests can use small, controlled data.

## Why Not Just Click?

*What are the problems with checking every route by opening a browser and clicking around?*

-   Every change means repeating the same steps by hand:
    -   Start the server
    -   Open the browser
    -   Visit the index page
    -   Click a detail link
    -   Try a made-up ID to see the 404
    -   Stop the server
-   Clicking is easy to rush or skip, so bugs slip through
-   The more routes the application has, the more steps there are to forget

*What do I need to install to test a Litestar application with pytest?*

-   `uv add pytest` adds the [pytest][pytest] testing framework
-   Litestar's test client uses the [httpx][httpx] library internally, so `uv add httpx` is needed too
-   Both packages are now available whenever you run pytest

## A First Test

*Write a pytest test file called `test_server1.py` that uses Litestar's TestClient to check that
`GET /` returns a 200 status code and that the page contains the text "Sasquatch Sightings".*

-   `TestClient` from `litestar.testing` is a [%g test-client "test client" %]:
    it wraps the application and lets you call routes directly in memory, with no real server or browser
-   `with TestClient(app=make_app()) as client:` sets up the client and tears it down cleanly
    at the end of the `with` block
-   `client.get("/")` sends a GET request and returns a response object
-   `response.status_code` holds the three-digit [%g status-code "status code" %]:
    200 means success, 404 means not found
-   `response.text` is the full body of the response as a plain string,
    which is all you need to check that the right content appeared
-   Run the tests from the `testserver/` directory with:

[%inc run_tests.sh %]

[%inc test_server1.py %]

## Testing Error Responses

*Add two more tests to `test_server1.py`: one that checks a valid sighting ID returns 200,
and one that checks a missing ID returns 404.*

-   Testing both the success path and the error path builds confidence that the code handles both correctly
    -   A route that never returns 404 when it should is just as broken as one that returns 200 when it should not
-   The 20 rows in `SIGHTINGS` use IDs 1 through 20,
    so ID 9999 is guaranteed to be missing and will trigger `raise NotFoundException`
-   pytest reports pass or fail for each function separately, so you can see at a glance which path broke

## A Testable Server

*What is the risk of writing a test like `assert "G. horribilus" in response.text`
when "G. horribilus" comes from the `SIGHTINGS` list in `dataset.py`?*

-   If someone updates `dataset.py` by correcting a species name, adding rows, or removing old ones,
    the test breaks even though the route is working correctly
-   A test that fails for the wrong reason wastes time and erodes trust in the whole test suite
-   The fix is to control exactly what data the server uses during the test

*Refactor `server3.py` into a new file `server4.py` by wrapping the route definitions in a function
called `make_app` that takes the sightings list as a parameter.*

-   `make_app(sightings=SIGHTINGS)` is a function that defines the route handlers and returns the app
    -   The default value means calling `make_app()` with no arguments behaves exactly like `server3.py`
    -   Calling `make_app(SMALL)` returns an app that serves `SMALL` instead of the full dataset
-   The handlers inside `make_app` use `sightings` just like any function uses a parameter:
    wherever `server3.py` wrote `for s in SIGHTINGS`, `server4.py` writes `for s in sightings`
-   `app = make_app()` at the bottom keeps `litestar run --app server4:app` working from the terminal

[%inc server4.py %]

## Testing with Controlled Data

*Write a second test file called `test_server2.py` that defines a two-row list called `SMALL`
and uses `make_app(SMALL)` to test the index links, the detail page content,
and the display of `None` values.*

-   `SMALL` has exactly two rows, so it is easy to see at a glance what each test is checking
-   `make_app(SMALL)` creates a fresh app that serves only those two rows
    -   Each test creates its own app, so there is no shared state between tests
-   `test_none_displayed_as_empty` confirms that a sighting with `sex=None` and `weight=None`
    does not show the word `"None"` anywhere in the page
    -   This is the kind of edge case that is easy to miss when clicking manually

[%inc test_server2.py %]

## Check Understanding

<details markdown="1">
<summary markdown="1">What is the difference between running `litestar run --app server4:app` and calling `client.get("/")` in a test?</summary>

`litestar run` starts a real server process that listens on port 8000 and waits for browser requests
over the network.
`client.get("/")` sends a request directly to the application in memory without any network connection.
Tests therefore run without a browser and without needing a free port.

</details>

<details markdown="1">
<summary markdown="1">Why does `server4.py` still have the line `app = make_app()` at the bottom?</summary>

`litestar run --app server4:app` looks for a module-level name called `app`.
Without that line, running the server from the terminal would fail with an import error.
The factory function is for tests; the module-level `app` is for the command line.

</details>

<details markdown="1">
<summary markdown="1">The code below raises an error when it runs. What is wrong and how do you fix it?</summary>

```python
client = TestClient(app=make_app())
response = client.get("/")
assert response.status_code == 200
```

`TestClient` must be used inside a `with` block.
The `with TestClient(app=make_app()) as client:` form ensures the client starts up and shuts down properly.
Calling `client.get()` before entering the `with` block raises a runtime error.
The fix is:

```python
with TestClient(app=make_app()) as client:
    response = client.get("/")
assert response.status_code == 200
```

</details>

<details markdown="1">
<summary markdown="1">A test uses `make_app(SMALL)` and checks `assert "G. canadensis" in response.text`.
A colleague adds a third row to `SMALL` with species `"G. horribilus"` for an unrelated test.
Does the first test break?</summary>

No.
The first test still passes because `"G. canadensis"` is still in the response.
Adding a row to `SMALL` only breaks a test if that test makes an assumption that breaks with more data,
such as asserting the page contains exactly two links.
This is another reason to keep assertions specific: check for what you expect to be there,
not for the absence of things you did not add.

</details>

<details markdown="1">
<summary markdown="1">The test below always fails, even when the route is working correctly. What is wrong?</summary>

```python
def test_detail_ok():
    with TestClient(app=make_app()) as client:
        response = client.get("/sighting/1")
    assert response.status_code == "200"
```

`response.status_code` is an integer, not a string.
Comparing it to the string `"200"` is always `False` in Python.
The fix is to drop the quotes: `assert response.status_code == 200`.

</details>

See [%b pytest2025 %] for the full pytest documentation and [%b litestar2025 %] for Litestar's testing reference.

## Exercises

### Test the CSS Route

Add a test to `test_server1.py` that sends `GET /style.css` and checks that the response
status code is 200 and that the response text contains the word `"table"`.

### Test a Specific Detail Page

Add a test using `make_app(SMALL)` that visits `/sighting/2` and confirms that the
text `"G. horribilus"` appears in the response.

### Test an Invalid Path Parameter

Visit `/sighting/abc` in a test and assert that the response status code is 400.
Look up what HTTP status code 400 means and write a comment in the test explaining why 400 is the
right code here rather than 404.

### Test Both Species in the Index

Write a test using `make_app(SMALL)` that visits the index page and asserts that both
`"G. canadensis"` and `"G. horribilus"` appear in the response text.

### Combine Two Assertions

Rewrite `test_index_returns_ok` and `test_index_contains_title` as a single test function
that makes both assertions using one `TestClient`.
When would it be better to keep them as two separate tests?
