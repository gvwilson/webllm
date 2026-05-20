# Glossary

## A

<span id="attribute">attribute</span>
:   A `name="value"` pair written inside an HTML opening tag that customizes
    or provides additional information about the element.
    For example, `href` in `<a href="...">` specifies where the link goes.

## B

## C

<span id="css">Cascading Style Sheets</span> (CSS)
:   A language for describing how HTML elements should be displayed,
    including fonts, colors, spacing, and layout.  "Cascading" refers
    to the rules that determine which style wins when more than one
    rule applies to the same element.

<span id="certificate">certificate</span>
:   A file that proves a server's identity during a secure connection.
    It contains the server's hostname, a public key used for encryption, and a digital signature
    from a certificate authority that vouches for its authenticity.
    Browsers check this signature before allowing an encrypted connection to proceed.

<span id="certificate-authority">certificate authority</span> (CA)
:   An organization that issues and digitally signs certificates, vouching for the identity of
    the server named in each certificate.
    Browsers ship with a built-in list of trusted CAs; a certificate signed by any of them is
    accepted without a warning.
    For local development, `mkcert` acts as a private CA whose root certificate you add to your
    own machine's trust store.

<span id="column">column</span>
:   A named field in a database table that holds one kind of value for every row.
    For example, the `sightings` table has columns named `species`, `sex`, and `weight`.
    Every row must have a value for each column, or store null if the value is unknown.

<span id="csv">comma-separated values</span> (CSV)
:   A plain-text file format for tabular data in which each line is one row and values
    within a row are separated by commas.
    The first line is usually a header row listing column names.
    Empty values are represented by two consecutive commas.

<span id="conftest-file">`conftest.py`</span>
:   A special file that pytest looks for automatically in the same directory as a test file
    (and in parent directories up to the project root).
    Fixtures defined in `conftest.py` are available to every test file in that directory
    without any import statement.

<span id="css-class">CSS class</span>
:   A label given to one or more HTML elements with the `class` attribute
    so that they can be styled as a group.
    In a stylesheet, a class selector begins with a dot: `.warning { color: red; }`.

<span id="css-property">CSS property</span>
:   A single stylistic setting in a CSS rule, such as `font-family: sans-serif`
    or `border: 1px solid gray`.

<span id="css-rule">CSS rule</span>
:   A block of CSS consisting of a selector and one or more property declarations
    in curly braces, such as `p { font-size: 1em; line-height: 1.5; }`.

<span id="css-selector">CSS selector</span>
:   The part of a CSS rule that identifies which HTML elements the rule applies to.
    `h1` selects all `<h1>` elements; `.note` selects all elements with `class="note"`;
    `#title` selects the element with `id="title"`.

## D

<span id="database">database</span>
:   An organized collection of data stored on disk so that it survives program restarts
    and can be shared across multiple programs or users.
    A SQL database organizes data into tables of rows and columns and provides a standard
    language for querying and updating that data.

## E

<span id="element">element</span>
:   A single unit of content in an HTML document, represented by an opening tag,
    optional content, and a closing tag.
    For example, `<p>A paragraph.</p>` is a paragraph element.

<span id="end-to-end-test">end-to-end test</span>
:   A test that drives the application through a real browser, sending actual HTTP requests
    and checking what the user sees on screen.
    Unlike a test client that talks directly to the server in memory,
    an end-to-end test exercises browser-side behavior such as form validation and JavaScript.

## F

<span id="file-path">file path</span>
:   A string that identifies the location of a file on a computer's filesystem,
    such as `./images/map.png`.
    A relative file path is interpreted starting from the location of the file that contains it,
    not from a fixed root, which means it works regardless of where the project is stored on disk.

<span id="fixture">fixture</span>
:   A function decorated with `@pytest.fixture` that sets up resources a test needs,
    such as a database connection or a temporary directory.
    pytest injects the fixture's return value into any test function that names the fixture
    as a parameter, and tears down the resource automatically when the test finishes.

<span id="form">form</span>
:   An HTML element that groups one or more inputs together with a submit button so the browser
    can collect values from the user and send them to the server.
    The `method` attribute specifies GET or POST, and `action` specifies the URL to send to.

## G

## H

<span id="headless">headless</span>
:   A mode in which a browser runs without displaying a visible window.
    Headless browsers are used in automated testing because they run faster and
    do not require a graphical display.
    Most browser testing tools default to headless mode and offer a flag to show the window
    for debugging.

<span id="html-entity">HTML entity</span>
:   A short code used in HTML to represent a character that would otherwise be
    interpreted as markup or is not easily typed.
    Entities begin with `&` and end with `;`, for example `&lt;` for `<`,
    `&amp;` for `&`, and `&copy;` for &copy;.

<span id="html-fragment">HTML fragment</span>
:   A snippet of HTML returned by a server that contains only the content needed to update
    part of an existing page, such as a handful of table rows or a detail panel.
    Unlike a full HTML page, a fragment has no `<html>`, `<head>`, or `<body>` tags.
    Libraries such as HTMX insert fragments directly into the appropriate place in the page
    without triggering a full reload.

<span id="htmx">HTMX</span>
:   A JavaScript library that adds interactivity to web pages through HTML attributes
    rather than custom JavaScript code.
    Attributes such as `hx-get`, `hx-trigger`, `hx-target`, and `hx-swap` tell the browser
    when to fetch a URL, what event should trigger the fetch, and where to insert the returned HTML fragment.

<span id="http-200">HTTP 200</span>
:   The HTTP status code a server returns when the request succeeded.

<span id="http-303">HTTP 303</span>
:   The HTTP status code a server returns to redirect the client to another URL.

<span id="http-404">HTTP 404</span>
:   The HTTP status code a server returns when it cannot find the resource the client requested.
    "404 Not Found" is so common that it has become shorthand for any missing page on the web.

<span id="http-request">HTTP request</span>
:   A message sent from a browser (or other client) to a web server asking for a resource.
    A GET request asks the server to return data; a POST request sends data to the server.
    Each request includes the URL path, any headers, and (for POST) a body.

<span id="http-response">HTTP response</span>
:   A message sent from a web server back to the browser in reply to an HTTP request.
    It includes a status code (200 for success, 404 for not found, etc.),
    headers such as the media type, and a body containing the requested content.

<span id="https">HTTPS</span> (Hypertext Transfer Protocol Secure)
:   An extension of HTTP that encrypts all traffic between the browser and the server using TLS.
    A URL beginning with `https://` signals that the connection is encrypted;
    browsers display a padlock icon to confirm this.
    HTTPS also requires the server to present a certificate so the browser can verify its identity.

<span id="html">HyperText Markup Language</span> (HTML)
:   The standard language for creating web pages.
    An HTML document describes content using nested elements marked by tags,
    and a browser renders those elements as visible text, images, and links.

## I

<span id="internal-style-sheet">internal stylesheet</span>
:   CSS rules written inside a `<style>` element in the `<head>` of an HTML page,
    as opposed to an external stylesheet in a separate `.css` file.
    An internal stylesheet is self-contained, so the page renders correctly
    when opened directly in a browser without a web server.

## J

## K

<span id="keyword-argument">keyword argument</span>
:   A function argument passed by name rather than by position, written as `name=value`.
    In htpy, keyword arguments set the attributes of an HTML element:
    `a(href="#recent")` sets the `href` attribute on the `<a>` tag.

## L

<span id="list-comprehension">list comprehension</span>
:   A compact Python expression that builds a new list by applying an expression to each item
    in an existing sequence: `[x * 2 for x in numbers]`.
    In htpy, list comprehensions are a natural way to generate one HTML element per row of data.

<span id="localhost">localhost (loopback address)</span>
:   The special IP address `127.0.0.1`, which always refers to the current machine.
    A web server listening on `localhost` only accepts requests from the same computer,
    not from other machines on the network.
    The name `localhost` is an alias for `127.0.0.1`.

<span id="locator">locator</span>
:   A description of which element on a page a browser testing tool should interact with,
    such as `"table a"` to mean "any link inside a table".
    Playwright evaluates locators lazily, just before an action is performed,
    so the element does not need to exist when the locator is created.

<span id="log-handler">log handler</span>
:   An object attached to a logger that decides where log messages go.
    Common handlers send messages to the terminal (`StreamHandler`),
    to a file (`FileHandler`), or to a size-limited file that rotates automatically
    (`RotatingFileHandler`).
    A single logger can have more than one handler,
    so the same message can appear in the terminal and in a file simultaneously.

<span id="log-level">log level</span>
:   A label that classifies the severity of a log message.
    Python's `logging` module defines five standard levels in increasing order of severity:
    `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.
    Setting the active level to `INFO`, for example, silences all `DEBUG` messages
    without changing any code.

<span id="logger">logger</span>
:   An object that records log messages on behalf of a module.
    Each module should create its own logger with `logging.getLogger(__name__)`,
    which names the logger after the module so that log entries can be traced back to their source.

## M

<span id="media-type">media type</span>
:   A label included in an HTTP response header that tells the browser what kind of content
    the response body contains.
    Common values are `text/html` for web pages, `text/css` for stylesheets,
    and `application/json` for JSON data.
    Browsers use the media type to decide how to render or process the response.

<span id="multipart">multipart encoding</span>
:   A way of packaging an HTTP request body into separate labelled sections, one for each
    form field, so that file contents can be sent alongside ordinary text values.
    Any form that includes a file input must use `enctype="multipart/form-data"` to trigger
    this encoding; without it the browser sends only the filename, not the file's contents.

## N

<span id="db-null">null (database)</span>
:   A special marker in a database column meaning "no value was recorded here."
    Null is not the same as zero, an empty string, or Python's `None`,
    though Python's `sqlite3` module represents SQL null as `None` when returning results.

## O

## P

<span id="path-parameter">path parameter</span>
:   A variable segment in a URL route pattern, written in curly braces, such as
    `{sighting_id:int}` in `/sighting/{sighting_id:int}`.
    The web framework extracts the value from the URL and passes it to the handler function.
    The optional type suffix (`:int`) tells the framework to convert the extracted text
    to the specified type before calling the function.

<span id="placeholder">placeholder</span>
:   A `?` marker in a SQL query that `sqlite3` replaces with a supplied value at runtime.
    Using placeholders instead of inserting values directly into the query string prevents
    SQL injection, a common attack in which a malicious value changes the meaning of the query.

<span id="port">port</span>
:   A number from 0 to 65535 that identifies a specific service on a networked computer,
    like a door number on a building.
    Web servers commonly listen on port 80 (HTTP) or 443 (HTTPS);
    local development servers typically use 8000 or 8080 to avoid requiring special permissions.

## Q

<span id="query">query</span>
:   A SQL instruction that retrieves or modifies data in a database.
    A query that reads data (beginning with `select`) returns a set of rows;
    a query that writes data (beginning with `insert`, `update`, or `delete`)
    changes the database and returns nothing.

## R

<span id="redirect">redirect</span>
:   An HTTP response that tells the browser to immediately send a new request to a different URL.
    A 303 "See Other" redirect is used after a POST request so that refreshing the page
    replays a safe GET rather than re-submitting the form and repeating the action.

<span id="root-element">root element</span>
:   The single outermost element in an HTML document that contains all other elements.
    In HTML this is the `<html>` element.

<span id="route">route</span>
:   A pairing of a URL pattern and a handler function in a web application.
    When the server receives a request, it matches the URL against its routes
    and calls the handler for the first match.
    For example, the route `GET /sighting/{id}` matches any GET request
    whose path starts with `/sighting/` followed by an identifier.

<span id="row">row</span>
:   A single record in a database table, containing one value (or null) for each column.
    A row in the `sightings` table represents one reported sasquatch observation.

## S

<span id="sql_injection">SQL injection</span>
:   An attack where a malicious user inserts SQL code into
    user-supplied input that gets executed as part of a database
    query.

<span id="status-code">status code</span>
:   The three-digit number at the start of an HTTP response that indicates whether the request
    succeeded or failed.
    200 means the server found and returned the content;
    400 means the request was malformed;
    404 means the requested resource was not found;
    500 means something went wrong on the server.

<span id="sql">Structured Query Language</span> (SQL)
:   The standard language for creating, querying, and modifying data in a relational database.
    SQL uses English-like keywords such as `select`, `insert`, `create table`, and `where`
    to describe what data to retrieve or change.

## T

<span id="db-table">table (database)</span>
:   A collection of rows in a database, where every row has the same named columns.
    A table is similar to a spreadsheet: each column has a fixed name and type,
    and each row is one record.

<span id="tag">tag</span>
:   The angle-bracket notation used to mark the start or end of an HTML element.
    An opening tag has the form `<tagname>` and a closing tag has the form `</tagname>`.

<span id="template-engine">template engine</span>
:   A tool that combines a template (an HTML file with placeholders) and data to produce
    a finished HTML document.
    [Jinja][jinja] is a popular Python template engine; it replaces `{{ variable }}` with the variable's
    value and handles loops and conditionals with `{% %}` blocks.

<span id="test-client">test client</span>
:   A tool that sends HTTP requests directly to a web application in memory,
    without starting a real server or opening a browser.
    The application handles requests normally, so tests can check status codes and response content
    without any network setup.

<span id="tls">TLS</span> (Transport Layer Security)
:   A protocol that encrypts the connection between a browser and a server so that
    data cannot be read or modified in transit.
    TLS is the mechanism that makes HTTPS secure; when you see a padlock in the browser,
    TLS is doing the work of protecting the connection.

<span id="tree">tree</span>
:   A data structure in which each item has at most one parent and any number of children,
    with a single root item at the top.
    HTML documents form a tree because elements must be properly nested.

## U

## V

<span id="void-element">void element</span>
:   An HTML element that has no content and therefore no closing tag, such as
    `<img>` or `<br>`.

## W

<span id="web-framework">web framework</span>
:   A library that handles the low-level details of receiving HTTP requests and sending responses,
    so developers can focus on application logic rather than network plumbing.
    Examples include FastHTML, Flask, and Django for Python.

<span id="web-server">web server</span>
:   A program that listens for HTTP requests from browsers or other clients and sends back responses.
    Unlike a static file server, a web server can generate different responses for different requests,
    read from databases, and accept data submitted through forms.

## X

## Y

## Z
