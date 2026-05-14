# Serving Data

## Goals

-   Understand what a web server does and how it differs from opening a file in a browser.
-   Use Litestar to create a route that returns a plain-text response.
-   Serve a single HTML page built with htpy and styled with an external CSS file.
-   Add a second page linked from the first.

## What a Web Server Does

*What is a web server and how is it different from opening an HTML file in a browser?*

-   When you double-click an HTML file, the browser reads it from disk: no network involved
-   A [%g web-server "web server" %] is a program that listens for requests from browsers
    and sends back responses
    -   The browser says "give me the page at `/sightings`"
    -   The server reads some data, builds a page, and sends it back
-   This matters because a server can generate different pages for different requests,
    read from a database, and accept form submissions, none of which work with static files

*What is Litestar and how do I add it to the project?*

-   [Litestar][litestar] is a Python [%g web-framework "web framework" %]:
    -   A library that handles the low-level details of receiving requests and sending responses
        so you can focus on your application logic
-   Add it to the project with `uv add litestar`, then confirm with `python -c "import litestar"`
-   A Litestar application is made of [%g route "routes" %]
    -   Each route pairs a URL pattern with the Python function that handles requests to that URL

## A First Server

*Write a Litestar server with a single route at `/` that returns the message
"Hello from the Sasquatch Observatory!".*

-   The `@get("/")` decorator marks the function as a handler for GET requests to `/`
-   The function's return [%g type-annotation "type annotation" %] (`-> str`)
    tells Litestar what kind of data to expect
-   `Litestar([index])` creates the application with a list of handlers
-   The `async` keyword tells Python this function can run while waiting on other work;
    Litestar works with both `async def` and plain `def`, but LLMs typically generate `async def`

[%inc server_hello.py %]

-   Run the server from inside the `litestar/` directory with the command below
    -   Stop it with Ctrl-C when you are done
    -   If it doesn't work, check that your uv environment is active

[%inc run1.sh %]

-   The terminal shows `Listening at http://127.0.0.1:8000`
    -   Visit that URL in a browser
-   `127.0.0.1` is the [%g localhost "loopback address" %] (also written as `localhost`)
    -   Your computer talking to itself rather than to a remote machine
-   `8000` is the [%g port "port" %] number, like a door number in a building
    -   Different programs listen on different ports so they do not collide

*Explain what happens step by step when the browser visits `http://127.0.0.1:8000`.*

-   The browser opens a connection to port 8000 on the loopback address
    and sends an [%g http-request "HTTP request" %]: "GET / HTTP/1.1"
-   Litestar matches the path `/` to the `index` function and calls it
-   The function returns the string, Litestar wraps it in an [%g http-response "HTTP response" %],
    and sends it back
-   With a [%g http-200 "200" %] status code to indicate that everything is OK
-   The browser displays the text in the window

<div class="callout" markdown="1">

### Why `index`?

The name `index` comes from the early web, when servers mapped URLs directly to files on disk.
`index.html` was like the index of a book.
Modern frameworks keep the convention: the function that handles requests for `/` is called `index`
because it serves the site's front page.

</div>

## A Table of Sightings

*Create a file called `dataset.py` containing twenty rows of synthetic sasquatch sighting data.
Each row must be a dict with keys for ID, species, sex, weight, color, date/time,
latitude, and longitude. Some sex and weight values should be `None` to represent
observations where those details were not recorded.*

-   The LLM produces a list of dicts
-   Store it in a variable called `SIGHTINGS`
-   Using `None` for missing values is more honest than using an empty string or zero,
    and it forces you to handle the missing case explicitly in the rest of the code

[%inc dataset.py head=11 %]

*Write a Litestar route at `/` that imports `SIGHTINGS` from `dataset.py` and returns
an HTML page with a table of all sightings*

-   Pass `media_type=MediaType.HTML` to `@get` so the browser renders the response as HTML
    rather than displaying the raw tags as text
-   Display `None` values as an empty string with `str(s[k]) if s[k] is not None else ""`

*Modify the Litestar route to Link to an external CSS file called `style.css`.
Also add a route at `/style.css` to read and return that file.*

-   Link to the stylesheet with `link(rel="stylesheet", href="/style.css")` in the `<head>`
-   When the browser parses that link it makes a second GET request to `/style.css`,
    so the server needs a route to handle it
-   The CSS route reads the file from disk relative to the server script using `Path(__file__).parent`

[%inc server_table.py %]

*Explain what `MediaType.HTML` does and what the browser would show if it was left out.*

-   HTTP responses carry a [%g media-type "media type" %] (sometimes called a MIME type)
    that tells the browser what kind of content it is receiving
-   `MediaType.HTML` sets that header to `text/html`; without it Litestar defaults to `text/plain`
-   With `text/plain` the browser treats the content as literal characters,
    so `<table>` appears on screen as `<table>` rather than becoming a rendered table

*Write a simple CSS stylesheet that sets the font and page width, puts borders on the table cells,
and makes the header row slightly gray.*

[%inc style.css %]

## Detail Pages

*Make each sighting ID in the table a link to `/sighting/{id}`.
Add a route that looks up that ID and displays the sighting's details
in a two-column table with the field names on the left and values on the right.*

-   A [%g path-parameter "path parameter" %] is a variable segment of the URL:
    `{sighting_id:int}` matches `/sighting/1`, `/sighting/2`, and so on,
    and Litestar converts the captured text to an integer before passing it to the handler
-   The handler loops through `SIGHTINGS` looking for the matching ID
    -   `raise NotFoundException(...)` sends a [%g http-404 "404 response" %] if none is found
-   The detail table has one row per field
-   Each sighting ID in the index table becomes a link:
    `a(href=f"/sighting/{s['id']}")[str(s["id"])]`

[%inc server_detail.py mark=index-with-links %]

[%inc server_detail.py mark=detail-route %]

[%inc run3.sh %]

*Trace what happens when a user visits `/sighting/99` and ID 99 is not in the data.*

-   Litestar matches the URL to `detail` and calls it with `sighting_id=99`
-   The `for` loop finishes without finding a match, so execution reaches `raise NotFoundException`
-   Litestar catches the exception and sends back an HTTP response with status code 404
-   The browser shows an error page
    -   No Python traceback appears in the browser window, but Litestar prints a log line in the terminal

## Check Understanding

<details markdown="1">
<summary markdown="1">What is the difference between `@get("/")` and `@get("/sightings")`?</summary>

Both decorate a function as a GET request handler, but they respond to different URLs.
`@get("/")` handles requests to `http://127.0.0.1:8000/` (the root),
while `@get("/sightings")` handles requests to `http://127.0.0.1:8000/sightings`.
A Litestar app can have as many routes as you like, each at a different path.

</details>

<details markdown="1">
<summary markdown="1">You visit `http://127.0.0.1:8000`, but the browser shows
"This site can't be reached". What is the most likely cause?</summary>

The server is not running: either you have not run `litestar run --app server_hello:app`,
or it crashed on startup, or you stopped it.
Check the terminal where you launched the server for error messages.

</details>

<details markdown="1">
<summary markdown="1">The code below is supposed to show an HTML page, but the browser displays the raw tags as text. What is wrong and how do you fix it?</summary>

```python
@get("/")
async def index() -> str:
    return str(html[body[p["Hello"]]])
```

The route is missing `media_type=MediaType.HTML`, so Litestar sends the response as `text/plain`.
The browser therefore treats the content as literal text rather than markup.
The fix is:

```python
@get("/", media_type=MediaType.HTML)
async def index() -> str:
    return str(html[body[p["Hello"]]])
```

</details>

<details markdown="1">
<summary markdown="1">Why does the browser make two requests when it loads the sightings table page?</summary>

The first request is for the page itself (`GET /`).
The HTML the server returns contains `<link rel="stylesheet" href="/style.css">`.
When the browser parses that tag, it automatically makes a second request (`GET /style.css`)
to fetch the stylesheet.
This is why `server_table.py` needs both an `index` route and a `styles` route.

</details>

<details markdown="1">
<summary markdown="1">The route below is supposed to display a sighting's details, but visiting
`/sighting/abc` crashes the server with an unhandled exception. Why, and how does adding `:int`
to the path parameter fix it?</summary>

```python
@get("/sighting/{sighting_id}")
async def detail(sighting_id: str) -> str:
    ...
```

Without `:int`, Litestar captures the URL segment as a plain string and passes it to the handler.
When the handler tries to compare it to the integer IDs in `SIGHTINGS` the logic may fail,
and any code that treats it as a number will raise a `ValueError` or `TypeError`.
Writing `{sighting_id:int}` tells Litestar to convert the segment to an integer before calling the handler.
If the segment is not a valid integer, such as `abc`, Litestar itself returns a 400 Bad Request response
before your function is ever called.

</details>

See [%b litestar2025 %] for the full Litestar documentation and [%b mdn-html2024 %] for the HTTP reference.

## Exercises

### Add a Heading to Every Page

Add an `<h1>` heading to the `<body>` of both the index page and the detail page in `server_detail.py`.
The index page heading should say "Sasquatch Sightings in British Columbia";
the detail page heading should include the sighting ID, for example "Sighting 7".

### Link Back from the Detail Page

The detail page already has a "Back to all sightings" link in `server_detail.py`.
Open `server_detail.py`, find where that link is built, and move it above the table
so it appears at the top of the page rather than below it.

### Filter by Species

Add a new route at `/species/{name}` that returns only the sightings whose `species` field
matches the given name. Display them in the same table format as the index page.
What happens if you visit `/species/G.%20canadensis`? (The `%20` is how a space appears in a URL.)

### Show a Count

Add a line below the table on the index page that displays the total number of sightings,
for example "20 sightings on record". Display it in a `<p>` element.

### Style None Differently

Instead of displaying `None` values as empty strings, display them as the word "unknown"
and add a CSS class `unknown` to those cells.
Add a rule to `style.css` that makes cells with class `unknown` appear in gray italic text.
