# Glossary

## A

<span id="attribute">attribute</span>
:   A `name="value"` pair written inside an HTML opening tag that customizes
    or provides additional information about the element.
    For example, `href` in `<a href="...">` specifies where the link goes.

## B

## C

<span id="css">CSS (Cascading Style Sheets)</span>
:   A language for describing how HTML elements should be displayed,
    including fonts, colors, spacing, and layout.  "Cascading" refers
    to the rules that determine which style wins when more than one
    rule applies to the same element.

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

## E

<span id="element">element</span>
:   A single unit of content in an HTML document, represented by an opening tag,
    optional content, and a closing tag.
    For example, `<p>A paragraph.</p>` is a paragraph element.

## F

<span id="file-path">file path</span>
:   A string that identifies the location of a file on a computer's filesystem,
    such as `./images/map.png`.
    A relative file path is interpreted starting from the location of the file that contains it,
    not from a fixed root, which means it works regardless of where the project is stored on disk.

## G

## H

<span id="html">HTML (HyperText Markup Language)</span>
:   The standard language for creating web pages.
    An HTML document describes content using nested elements marked by tags,
    and a browser renders those elements as visible text, images, and links.

<span id="html-entity">HTML entity</span>
:   A short code used in HTML to represent a character that would otherwise be
    interpreted as markup or is not easily typed.
    Entities begin with `&` and end with `;`, for example `&lt;` for `<`,
    `&amp;` for `&`, and `&copy;` for &copy;.

<span id="http-404">HTTP 404</span>
:   The HTTP status code a server returns when it cannot find the resource the client requested.
    "404 Not Found" is so common that it has become shorthand for any missing page on the web.
    Servers return other status codes for other problems: 500 for an internal server error,
    403 for a resource the client is not allowed to see.

<span id="http-request">HTTP request</span>
:   A message sent from a browser (or other client) to a web server asking for a resource.
    A GET request asks the server to return data; a POST request sends data to the server.
    Each request includes the URL path, any headers, and (for POST) a body.

<span id="http-response">HTTP response</span>
:   A message sent from a web server back to the browser in reply to an HTTP request.
    It includes a status code (200 for success, 404 for not found, etc.),
    headers such as the media type, and a body containing the requested content.

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

## M

<span id="media-type">media type</span>
:   A label included in an HTTP response header that tells the browser what kind of content
    the response body contains.
    Common values are `text/html` for web pages, `text/css` for stylesheets,
    and `application/json` for JSON data.
    Browsers use the media type to decide how to render or process the response.

## N

## O

## P

<span id="path-parameter">path parameter</span>
:   A variable segment in a URL route pattern, written in curly braces, such as
    `{sighting_id:int}` in `/sighting/{sighting_id:int}`.
    The web framework extracts the value from the URL and passes it to the handler function.
    The optional type suffix (`:int`) tells the framework to convert the extracted text
    to the specified type before calling the function.

<span id="port">port</span>
:   A number from 0 to 65535 that identifies a specific service on a networked computer,
    like a door number on a building.
    Web servers commonly listen on port 80 (HTTP) or 443 (HTTPS);
    local development servers typically use 8000 or 8080 to avoid requiring special permissions.

## Q

## R

<span id="root-element">root element</span>
:   The single outermost element in an HTML document that contains all other elements.
    In HTML this is the `<html>` element.

<span id="route">route</span>
:   A pairing of a URL pattern and a handler function in a web application.
    When the server receives a request, it matches the URL against its routes
    and calls the handler for the first match.
    For example, the route `GET /sighting/{id}` matches any GET request
    whose path starts with `/sighting/` followed by an identifier.

## S

## T

<span id="tag">tag</span>
:   The angle-bracket notation used to mark the start or end of an HTML element.
    An opening tag has the form `<tagname>` and a closing tag has the form `</tagname>`.

<span id="template-engine">template engine</span>
:   A tool that combines a template---an HTML file with placeholders---and data to produce
    a finished HTML document.
    Jinja is a popular Python template engine; it replaces `{{ variable }}` with the variable's
    value and handles loops and conditionals with `{% %}` blocks.

<span id="tree">tree</span>
:   A data structure in which each item has at most one parent and any number of children,
    with a single root item at the top.
    HTML documents form a tree because elements must be properly nested.

<span id="type-annotation">type annotation</span>
:   An optional label added to a Python function parameter or return value to indicate what type
    of data is expected, written with a colon for parameters and `->` for return values:
    `def greet(name: str) -> str:`.
    Python does not enforce annotations at runtime, but web frameworks like Litestar use them
    to validate incoming data and generate documentation automatically.

## U

## V

<span id="void-element">void element</span>
:   An HTML element that has no content and therefore no closing tag, such as
    `<img>` or `<br>`.

## W

<span id="web-framework">web framework</span>
:   A library that handles the low-level details of receiving HTTP requests and sending responses,
    so developers can focus on application logic rather than network plumbing.
    Examples include Litestar, Flask, and Django for Python.

<span id="web-server">web server</span>
:   A program that listens for HTTP requests from browsers or other clients and sends back responses.
    Unlike a static file server, a web server can generate different responses for different requests,
    read from databases, and accept data submitted through forms.

## X

## Y

## Z
