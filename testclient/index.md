# Testing with a Browser

## Goals

-   Understand why browser testing catches problems that HTTP-level testing misses.
-   Install pytest-playwright and download the browser binaries it needs.
-   Start a real server so Playwright has something to connect to.
-   Use Playwright to navigate pages and check their content.
-   Use Playwright to fill in and submit a form.

## Why Test in a Browser?

*What kinds of bugs can a browser catch that Litestar's test client cannot?*

-   The test client from the previous lessons sends HTTP requests directly to the application in memory:
    it never runs a real browser
    -   Browser-side validation is invisible to it: a form field marked `required` will refuse
        submission if left empty, but the test client bypasses that check entirely and sends
        whatever data it likes
    -   Any JavaScript that modifies the page after it loads is also invisible:
        the test client sees only the raw HTML the server sent, not what the browser does with it
-   [%g end-to-end-test "End-to-end testing" %] drives a real browser through real pages
    -   If something would block a user, it should block the test too
-   [Playwright][playwright-python] is a library that remote-controls browsers from Python
    -   Navigate to URLs, click buttons, fill in text fields, and read what the browser shows

*What do I need to install to run Playwright tests with pytest?*

-   `uv add pytest-playwright` adds the Playwright library and a pytest plugin
    that provides browser fixtures automatically
-   `playwright install firefox` downloads the Firefox browser binary that Playwright will control
    -   Playwright bundles its own browser rather than using the one already installed on your machine,
        so the behavior is the same on every computer
    -   Playwright also supports Chromium and WebKit, but one browser is enough to start
-   By default Playwright runs the browser invisibly in the background,
    which is called [%g headless "headless mode" %]
    -   `--headed` shows the browser window, which is useful when writing new tests
        or chasing down a failure

## Starting a Server for Tests

*What is the difference between tests that use Litestar's test client and tests that use Playwright?*

-   The test client talks directly to the application object in Python memory
    -   no network connection, no open port, no running process
-   Playwright controls a real browser that sends real HTTP requests,
    so there must be a real server listening on a real port before any test can run
-   `subprocess.Popen` starts a separate process from inside Python,
    exactly as if you had typed the command in a terminal

*What does `scope="session"` mean for a pytest fixture, and why use it for a server?*

-   By default a fixture has `scope="function"`, which means pytest creates a fresh copy for every
    test function and tears it down when that function finishes
    -   That is the right choice for a database: each test should start with clean data
-   `scope="session"` creates the fixture once for the entire test run and tears it down only
    after the last test finishes
    -   Starting and stopping a real server process for each test would add seconds per test;
        session scope means the cost is paid once
    -   Unlike a function-scoped fixture, a session-scoped fixture is shared across all tests,
        so tests that modify data will see each other's changes

*Write a `conftest.py` with a session-scoped fixture called `server_url` that starts
`server_pw.py` and shuts it down after all tests finish.*

-   `subprocess.Popen(["uv", "run", "litestar", "run", "--app", "server_pw:app"], cwd=LESSON_DIR)`
    starts the server as a separate process, just as if you had typed the command in a terminal
    -   `cwd=LESSON_DIR` runs the command in the directory where `server_pw.py` lives
-   `time.sleep(1.5)` gives the server a moment to start accepting connections before the first
    test sends a request
-   `yield "http://localhost:8000"` passes the URL to each test;
    the code after `yield` runs when the session ends, like the teardown half of a `with` block
-   `proc.terminate()` and `proc.wait()` stop the process cleanly when the session ends;
    `wait()` blocks until the process has fully exited so the port is free before anything else
    tries to use it

[%inc conftest.py %]

## Navigating Pages

*Copy the server from the forms lesson into this directory as `server_pw.py`.*

-   The server already supports every route the Playwright tests will use:
    index, detail, delete, add form, and CSV upload
-   No changes to the server are needed for Playwright testing

[%inc server_pw.py %]

*Write a test file called `test_browser.py` with a single test that opens the home page
and checks its title.*

-   `page` is provided by pytest-playwright: it represents a single browser tab,
    created fresh for each test function
-   `page.goto(server_url)` tells the browser to load that URL, just as a user would type it
-   `page.title()` returns the text from the `<title>` element,
    matching what the browser's title bar shows

*Add two more tests: one that confirms the sightings table is present, and one that clicks
a row link and waits for the detail page to load.*

-   `page.locator("table")` finds all `<table>` elements on the page;
    `.count()` returns how many there are
    -   A [%g locator "locator" %] is a description of which element to target,
        evaluated lazily just before Playwright acts on it
    -   `page.locator("table a").first` finds the first `<a>` inside any `<table>`,
        which picks out the sighting ID links and ignores the navigation links below the table
-   `.click()` simulates a left mouse click on the element
-   `page.wait_for_url("**/sighting/**")` pauses until the browser's address bar matches
    the pattern before moving on
    -   `**` matches any sequence of characters including slashes
    -   Without this wait, the assertion might run before the browser has finished
        loading the new page

## Filling in a Form

*How does Playwright simulate typing in a form field, and how do you select which field to target?*

-   `page.fill('[name="species"]', "G. canadensis")` finds the input whose `name` attribute
    is `species` and types the value into it, firing the same keyboard events a real user would
    -   `[name="species"]` is a CSS attribute selector: it matches any element whose `name`
        attribute equals `species`
    -   Required fields still prevent submission if left empty, because Playwright interacts
        with the browser's own validation the same way a user would

*Add a test to `test_browser.py` that opens the add-sighting form, fills in the required fields,
submits the form, and confirms the browser ends up back on the home page.*

-   `page.click('[type="submit"]')` clicks the submit button, which triggers the form POST
    -   The server processes the request and responds with a 303 redirect to `/`
    -   Playwright follows the redirect automatically, just as a real browser would
-   `page.wait_for_url(server_url + "/")` waits until the URL has changed to the home page
    before the assertion runs, so the test does not check the URL too early

[%inc test_browser.py %]

Run the tests from the `testclient/` directory:

[%inc run_tests.sh %]

See [%b playwright2025 %] for the full Playwright for Python documentation.

## Check Understanding

<details markdown="1">
<summary markdown="1">A classmate writes `client.post("/add", data={...})` with Litestar's TestClient to test the add form. What does this test confirm, and what does it miss?</summary>

The TestClient test confirms that the server receives the POST request,
inserts the row into the database,
and returns a 303 redirect.
It does not confirm that the `required` attribute on the form actually stops an empty field from being submitted, because that check happens in the browser before the request is ever sent.
A Playwright test is needed to verify browser-side behavior.

</details>

<details markdown="1">
<summary markdown="1">Why does the `server_url` fixture use `scope="session"` rather than the default scope?</summary>

The default scope is `"function"`, which creates and tears down the fixture for every test function.
Starting and stopping a real server process for each test would add several seconds per test
and make the suite impractical.
`scope="session"` creates the fixture once,
shares it with all tests,
and tears it down only after the last one finishes.

</details>

<details markdown="1">
<summary markdown="1">The test below fails intermittently: it passes on a fast machine and fails on a slow one. What is the most likely cause, and how do you fix it?</summary>

```python
def test_click_link(page, server_url):
    page.goto(server_url)
    page.locator("table a").first.click()
    assert "Sighting" in page.title()
```

After `.click()`, the browser sends the request and starts loading the detail page, but the assertion may run before the new page has finished loading.
On a fast machine the timing happens to work out; on a slow one it reads the old title and fails.
Adding `page.wait_for_url("**/sighting/**")` after the click tells Playwright to pause until the navigation is complete before reading the title.

</details>

<details markdown="1">
<summary markdown="1">After `proc.terminate()`, why does `conftest.py` also call `proc.wait()`?</summary>

`proc.terminate()` sends a signal telling the server process to stop,
but the process may take a moment to actually exit.
Without `proc.wait()`, the next test run might start before the old server has released port 8000,
causing a "port already in use" error.
`proc.wait()` blocks until the process has completely stopped,
so the port is free before the session teardown finishes.

</details>

<details markdown="1">
<summary markdown="1">The add-sighting test fills in species, color, datetime, latitude, and longitude but leaves sex and weight blank. Will the form submit successfully, and why?</summary>

Yes.
The sex and weight fields do not have the `required` attribute, so the browser allows submission with those fields empty.
The server receives empty strings for those fields and converts them to `None` before inserting into the database.
The test confirms the round trip worked by checking that the browser ended up back on the home page.

</details>

## Exercises

### Test the Delete Button

Write a test that navigates to a sighting detail page, clicks "Delete this sighting",
waits for the browser to return to the home page,
and confirms that the deleted sighting's ID no longer appears as a link in the table.

### Test a Missing Sighting

Write a test that visits `/sighting/9999` and confirms the page title is not "Sasquatch Sightings".
Run the test first with `--headed` to see what the browser actually shows for an error page,
then write an assertion based on what you observe.

### Verify Required Field Enforcement

Without calling `page.fill` for the species field, call `page.click('[type="submit"]')` on the
add form and assert that `page.url` is still the `/add` URL afterward.
This confirms the browser refused to submit the form because a required field was empty.

### Test the CSV Upload Form

Write a test that navigates to `/upload`, attaches the `sample.csv` file from the forms lesson
using `page.set_input_files('[name="csv_file"]', path_to_csv)`, clicks Upload, and confirms
the browser returns to the home page.
