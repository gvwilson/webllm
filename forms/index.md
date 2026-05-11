# Forms

## Goals

-   Understand how HTML forms send data to a server using POST requests.
-   Add a route that deletes a sighting when a user clicks a button.
-   Add routes that let a user fill in a form to add a new sighting.
-   Add routes that let a user upload a CSV file to add many sightings at once.
-   Test routes that modify the database.

## Deleting a Record

*What is the difference between a GET request and a POST request?*

-   Every HTTP request uses a method that tells the server what the client wants to do
-   GET asks the server to return data without changing anything
    -   Browsers send GET requests when a user types a URL or clicks a link
-   POST asks the server to process data the browser is sending, usually by writing to a database
    -   Browsers send POST requests when a user submits a form
-   Deleting a record must use POST, not GET
    -   Search engines and browser prefetch features send GET requests to URLs they discover automatically
    -   If a link could trigger a deletion, those tools could wipe out data without anyone asking them to

*Modify `server_db.py` to create `server_delete.py`. Add a Delete button to the sighting detail
page that sends a POST request to remove the sighting and then sends the browser back to the home page.*

-   An HTML [%g form "form" %] groups one or more inputs together with a submit button
    -   `<form method="post" action="/delete/1">` sends a POST request to `/delete/1` when submitted
    -   A `<button type="submit">` inside the form triggers the submission when clicked
    -   This form needs no text inputs: the sighting ID is already in the URL
-   `@post` in Litestar marks a handler that responds to POST requests,
    just as `@get` marks one that responds to GET
-   `delete from sightings where id = ?` removes the matching row; `conn.commit()` writes the change to disk
-   After deleting, the handler returns a [%g redirect "redirect" %] that tells the browser to fetch another URL
    -   `Redirect("/", status_code=303)` sends the browser to the home page
    -   This is called the Post/Redirect/Get pattern
    -   If the user presses Refresh afterward, the browser replays the GET, not the POST,
        so the record is not deleted a second time

[%inc server_delete.py %]

## Adding a Record

*Add a link to the home page and a `GET /add` route that displays a form for adding a new sighting.
Save the result as `server_add.py`.*

-   `<form method="post" action="/add">` sends the completed form to `/add` when submitted
-   `<input type="text" name="species" required>` creates a one-line text box
    -   The `name` attribute is the key the browser uses when sending the field to the server
    -   `required` tells the browser to refuse to submit the form if this field is empty
-   `<input type="number" name="latitude" step="0.01">` creates a number box that only accepts numeric input
    -   `step="0.01"` allows values with up to two decimal places;
        without it, only whole numbers are accepted
-   Optional fields like `sex` and `weight` omit `required`,
    so the form can be submitted even when they are blank

*Add a `POST /add` route to `server_add.py` that reads the submitted form data, inserts a new row,
and redirects the user to the home page.*

-   When a form is submitted, the browser encodes its fields as
    `species=G.+canadensis&color=brown&...` and sends them in the request body
-   Litestar decodes these into a dictionary when the handler is annotated with
    `Body(media_type=RequestEncodingType.URL_ENCODED)`
    -   `data["species"]` reads the field whose `name` attribute is `"species"` in the form
    -   Optional fields left blank arrive as empty strings;
        `data["sex"] or None` converts them to `None` before inserting into the database
    -   Number fields also arrive as strings; `float(data["latitude"])` converts them before inserting

[%inc server_add.py %]

## Uploading Many Records at Once

*What does a form look like when it needs to send a file instead of typed text,
and how does the server receive and parse the contents?*

-   File uploads require `enctype="multipart/form-data"` on the `<form>` tag
    -   Without this attribute the browser sends only the filename, not the file's contents
    -   [%g multipart "Multipart" %] encoding splits the request into separate labelled sections,
        one for each field, with file contents in their own section
-   `<input type="file" name="csv_file" accept=".csv">` adds a file picker to the form
    -   `accept=".csv"` filters the file picker to show only CSV files by default
-   [%g csv "CSV" %] (comma-separated values) is a plain-text format for tabular data
    -   The first line lists column names; each subsequent line is one row of data
    -   Empty values appear as two consecutive commas

*Add `GET /upload` and `POST /upload` routes to `server_add.py` to create `server_upload.py`.
The GET route should show a file upload form; the POST route should read the CSV and insert
all its rows into the database.*

-   Litestar receives the uploaded file through a `dataclass` whose field names match
    the `name` attributes in the form
    -   `await data.csv_file.read()` returns the file contents as `bytes`
    -   `.decode("utf-8")` converts them to a string that the `csv` module can read
-   `csv.DictReader` turns the string into an iterator of dictionaries, one per data row,
    using the header line for the keys
    -   `io.StringIO` wraps the string so `DictReader` treats it like a file
-   One `conn.commit()` at the end saves all the new rows in a single write to disk

[%inc server_upload.py %]

A sample CSV for testing the upload:

[%inc sample.csv %]

Start the server:

[%inc run.sh %]

## Testing Routes That Change Data

*How do you test a route that deletes a row from the database?*

-   Reuse the `small_db` fixture from the previous lesson to give each test a fresh temporary database
-   Send the POST request with `client.post("/delete/1")`
-   After the `with` block closes the client, open the database directly with `sqlite3.connect`
    and count the rows
    -   This checks the actual database state, not just what the server put in the response
-   A helper function `count_rows(db_path)` avoids repeating the connect-query-close pattern
    in every test

*Write tests for the add route and the CSV upload route in `test_server_forms.py`.*

-   `client.post("/add", data={...})` sends URL-encoded form data, exactly as a browser would
    -   Keys in `data` must match the `name` attributes on the form's `<input>` elements
    -   Pass empty strings for optional fields the user would leave blank
-   `client.post("/upload", files={"csv_file": ("upload.csv", content, "text/csv")})` sends
    a multipart request with a file attached
    -   The tuple contains the filename, the file contents as bytes, and the media type

[%inc test_server_forms.py %]

Run the tests from the `forms/` directory:

[%inc run_tests.sh %]

See [%b mdn-forms2025 %] for the HTML forms reference and [%b python-csv2025 %]
for the Python `csv` module documentation.

## Check Understanding

<details markdown="1">
<summary markdown="1">A classmate adds a Delete link rather than a button: `<a href="/delete/5">Delete</a>`. What goes wrong, and how do you fix it?</summary>

A link sends a GET request, not a POST request.
The server should never delete data in response to a GET, because search engines,
browsers, and prefetch tools send GET requests automatically.
The fix is to wrap a `<button type="submit">` inside
`<form method="post" action="/delete/5">`.

</details>

<details markdown="1">
<summary markdown="1">The weight field is left blank when a user submits the add form. The handler stores `data["weight"]` directly in the database. What does the database contain, and why is that a problem?</summary>

An empty form field sends the empty string `""` to the server, so the database stores `""`.
An empty string is not the same as SQL null: it is a string with no characters,
not a missing value.
The fix is `float(data["weight"]) if data["weight"] else None`,
which converts an empty string to `None`.
Python's `sqlite3` module stores `None` as SQL null.

</details>

<details markdown="1">
<summary markdown="1">The CSV file uses the header `Species` (capital S) but the handler reads `row["species"]` (lowercase s). What happens?</summary>

Python's dictionary lookup is case-sensitive, so `row["species"]` raises a `KeyError`.
The header in the CSV must exactly match the key the handler uses.
The simplest fix is to use the exact header from the CSV; a more robust fix converts
all header names to lowercase when reading the file.

</details>

<details markdown="1">
<summary markdown="1">Moving `conn.commit()` inside the loop so it runs after every insert changes the behavior. When does this matter, and when does it not?</summary>

Either way, all rows that were inserted successfully end up in the database.
The difference is what happens if the server crashes mid-upload.
Committing once at the end means no rows are saved if the crash happens before
the commit: the database is unchanged.
Committing after every insert means every row committed before the crash stays,
leaving partial data in the database.
For a small CSV in a tutorial, the difference is unnoticeable.

</details>

## Exercises

### Add a Confirmation Step

Modify the delete route so that clicking "Delete this sighting" first shows a page asking
"Are you sure?" with Confirm and Cancel buttons.
Only delete the row if the user clicks Confirm.

### Validate the Input Before Inserting

The add handler trusts that latitude is between -90 and 90 and longitude is between -180 and 180.
Add a check in the `POST /add` handler that returns an error message if either value is out of range,
without inserting any row.

### Report Upload Errors

If a row in the CSV is missing a required field, the handler raises an unhandled error.
Modify it to skip bad rows and return a page that lists which row numbers were skipped and why.

### Edit an Existing Record

Add a `GET /edit/{id}` route that shows a form pre-filled with the current values of a sighting,
and a `POST /edit/{id}` route that updates the row in the database with the submitted values.
