# Dynamic Pages

## Goals

-   Understand how HTMX lets the browser swap content into a page without a full reload.
-   Add a scrollable table that fetches more rows from the server as the user scrolls down.
-   Show a detail pane below the table that updates when the user clicks on any row.
-   Write server routes that return HTML fragments instead of complete pages.

## What Is HTMX?

> What problem does HTMX solve, and what would the same interaction look like without it?

-   Every page built so far responds to user actions by reloading the entire page
    -   Clicking a link sends a GET request, and submitting a form sends a POST request
    -   In both cases the browser discards everything it has and renders a fresh page from scratch
-   If you want to show a record's details when the user clicks a row,
    the obvious approach is to link to a full detail page
    -   But that throws away the scroll position in the table
-   [%g htmx "HTMX" %] is a JavaScript library that adds new behaviors to HTML elements through attributes
    -   Instead of reloading the whole page,
        HTMX sends a request to the server
        and inserts the returned content into one part of the existing page
-   The server returns an [%g html-fragment "HTML fragment" %]
    -   Just the new rows or the updated panel, not a complete HTML page
    -   No build step, no bundler, no JavaScript to write: the behaviors live in the HTML attributes

> How does HTMX get loaded, and what does a minimal HTMX attribute look like?

-   HTMX is loaded with a single `<script>` tag pointing to a content delivery network (CDN):

```html
<script src="https://unpkg.com/htmx.org@2.0.4"></script>
```

-   Once loaded, HTMX scans the page for attributes that start with `hx-`
    -   `hx-get="/some/url"`: when this element is triggered, fetch that URL
    -   `hx-trigger` determines what causes the fetch: `"click"`, `"change"`, `"revealed"`, and so on
    -   `hx-target` selects which element in the page receives the response
    -   `hx-swap` controls how the response is inserted:
        `"innerHTML"` replaces the target's contents,
        `"outerHTML"` replaces the target element itself
-   In htpy, attribute names with hyphens are written with underscores: `hx_get`, `hx_trigger`, `hx_swap`
    -   htpy converts them back to hyphens in the generated HTML

## Loading More Rows on Scroll

> Create a server that shows the first 20 sightings in a fixed-height scrollable table.
> When the user scrolls to the bottom, the table should automatically request and display the next 20 rows.

-   The table sits inside a `<div class="scroll-container">` whose CSS sets `height: 400px`
    and `overflow-y: scroll`, so only a few rows are visible at a time
-   The last `<tr>` in the table body is a sentinel row that carries three HTMX attributes:
    -   `hx-get="/rows?offset=20"`: the URL to fetch when this row becomes visible
    -   `hx-trigger="revealed"`: fire when this element scrolls into the visible area of its container
    -   `hx-swap="outerHTML"`: replace the sentinel row itself with whatever the server returns
-   `PAGE_SIZE = 20` is a named constant shared by `make_row`, `make_sentinel`, and both routes
    -   Using a named constant rather than a bare `20` means changing one line adjusts the whole server

> What does the `/rows` route return, and how does it know when to stop adding sentinels?

-   `/rows?offset=N` fetches the next page of rows from the database and returns raw `<tr>` elements
    -   No `<html>`, `<head>`, or `<body>` tags: just the rows
    -   HTMX swaps this fragment directly into the table, replacing the sentinel with the new rows
-   If the page returned has exactly `PAGE_SIZE` rows, there may be more;
    the route appends a new sentinel row with `offset` incremented by `PAGE_SIZE`
-   If the page has fewer than `PAGE_SIZE` rows, this is the last page;
    no sentinel is added and scrolling stops

[%inc server_scroll.py mark=helpers %]

[%inc server_scroll.py mark=index-route %]

[%inc server_scroll.py mark=more-rows %]

-   Start the server from the `htmx/` directory:

[%inc run.sh %]

-   Open `http://localhost:8000` and scroll to the bottom of the table
    -   The browser requests the next page without any page reload
    -   The new rows appear at the bottom as the old sentinel disappears

## Showing a Detail Pane on Click

> Add a panel below the table that shows the full record for any row the user clicks.
> The panel must update in place without reloading the page or affecting the scroll position.

-   Copy `server_scroll.py` to `server_detail.py` and make two changes to the page
-   Each data row gets three HTMX attributes:
    -   `hx-get="/sighting/{id}/detail"`: the URL to fetch when this row is clicked
    -   `hx-target="#detail"`: the CSS selector of the element to update
    -   `hx-swap="innerHTML"`: replace the contents of `#detail`, leaving the element itself in place
-   The page adds `<div id="detail" class="detail-pane">` below the scroll container,
    starting with a placeholder message
-   The CSS rule `tr[hx-target]:hover` gives the rows a pointer cursor and a highlight color,
    so users know the rows are clickable
    -   `tr[hx-target]` is an attribute selector that matches any `<tr>` that has an `hx-target` attribute
    -   In `server_scroll.py` no rows have `hx-target`, so this rule has no effect there

> Write the server route that returns the detail fragment.

-   `GET /sighting/{sighting_id}/detail` queries the database for one record
    and returns a `<table>` of field-value pairs with no surrounding page structure
    -   HTMX drops this directly into `#detail`, replacing whatever was there before
    -   The scroll position in the table is unchanged because HTMX only touched `#detail`,
        which sits below the scroll container
-   If the sighting ID does not exist, the route returns `<p>Sighting not found.</p>`
    -   A plain paragraph is enough; a full HTML error page would look broken inside the detail pane

[%inc server_detail.py mark=make-row %]

[%inc server_detail.py mark=index %]

[%inc server_detail.py mark=detail-fragment %]

See [%b htmx2025 %] for the full HTMX attribute reference.

## Check Understanding

<details markdown="1">
<summary markdown="1">A classmate adds `hx-trigger="click"` to the sentinel row by mistake. What happens when the user scrolls, and what should the sentinel's trigger be?</summary>

The sentinel no longer fires when scrolled into view, so no additional rows ever load.
The user sees only the first 20 rows regardless of how far they scroll,
with the "Loading..." sentinel sitting at the bottom doing nothing.
The correct trigger is `hx-trigger="revealed"`, which fires when the element enters the visible area.

</details>

<details markdown="1">
<summary markdown="1">The `/rows` route below always appends a sentinel, even when it fetches the last rows. What does the user see, and what extra work does the server do?</summary>

The sentinel appears after the last real row.
When the user scrolls to it, the browser sends one more request to `/rows?offset=...`.
The server queries the database, finds zero rows, and returns an empty string.
HTMX replaces the sentinel with the empty string, which removes it.
The user sees the sentinel flicker briefly; the server does one unnecessary database query per table load.
The fix is to only append the sentinel when `len(rows) == PAGE_SIZE`.

</details>

```python
result = "".join(str(make_row(row)) for row in rows)
result += str(make_sentinel(offset + PAGE_SIZE))
return result
```

<details markdown="1">
<summary markdown="1">Change `hx-swap="innerHTML"` on each data row to `hx-swap="outerHTML"`. What goes wrong after the first click?</summary>

`outerHTML` replaces the entire `#detail` element, not just its contents.
After the first click, the `<div id="detail">` no longer exists in the page.
Subsequent clicks still send a request,
but HTMX cannot find a `#detail` element to insert into,
so nothing appears.
`innerHTML` is correct because it leaves the target element in place and only changes what is inside it.

</details>

<details markdown="1">
<summary markdown="1">The detail pane shows "Sighting not found." even though the record definitely exists. What are two likely causes?</summary>

Either the row's `hx-get` attribute contains the wrong sighting ID
(perhaps `row["id"]` was formatted incorrectly),
or the `/sighting/{sighting_id}/detail` route is looking in a different database file
than the one populated with data.
Check the URL by inspecting the element in the browser's developer tools,
then verify that `DB_PATH` in the server points to the same database the other lessons use.

</details>

<details markdown="1">
<summary markdown="1">Why does `tr[hx-target]:hover` in the CSS correctly highlight only the clickable rows in `server_detail.py` but have no effect in `server_scroll.py`?</summary>

`tr[hx-target]` is a CSS attribute selector that matches `<tr>` elements which have an `hx-target` attribute.
In `server_detail.py`, each data row carries `hx-target="#detail"`, so the selector matches them.
In `server_scroll.py`, `make_row` adds no HTMX attributes to data rows at all,
so no `<tr>` has `hx-target` and the rule matches nothing.

</details>

## Exercises

### Replace the Sentinel with a Button

Change the sentinel row to a "Load more" button that the user must click to fetch the next page.
Replace `hx-trigger="revealed"` with `hx-trigger="click"` and style the button to span all eight columns.
Compare the user experience with and without the automatic trigger.

### Show a Loading Indicator

Add an `hx-indicator` attribute to the sentinel row pointing to a `<span>` element that shows
the text "Loading..." and is hidden by default using the CSS class `htmx-indicator`.
HTMX adds this class to the indicator while a request is in flight and removes it when the response arrives.
Confirm that the indicator appears briefly as each page loads.

### Highlight the Selected Row

When the user clicks a row to load its detail, give that row a visual marker so they can see
which record is currently displayed.
Add a `selected` CSS class with a distinct background color and use the `hx-on:htmx:after-swap`
attribute on `#detail` to remove the class from any previously selected row and add it to the new one.

### Filter by Species

Add a `<select>` element above the table listing the two species.
Use `hx-get="/?species=..."` and `hx-trigger="change"` on the select to reload just the `<tbody>`
when the user picks a different species.
Update the index route to accept an optional `species` query parameter
and filter the database query accordingly.
