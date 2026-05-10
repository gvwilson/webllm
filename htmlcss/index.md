# HTML and CSS

## Goals

-   Understand what HTML and CSS are and how they work together.
-   Create a valid HTML page with proper structure.
-   Use HTML entities to include characters that would otherwise confuse the browser.
-   Link between pages and to specific spots within a page.
-   Style a page with an internal stylesheet.
-   Use CSS classes to apply styles selectively.

## What HTML Looks Like

*Show me a simple HTML page about Sasquatch sightings with a heading, a paragraph, and a list.*

-   [%g html "HyperText Markup Language" %] (HTML) is the language browsers use to display content
-   An HTML document is made of [%g element "elements" %] marked by [%g tag "tags" %]
    -   An opening tag `<tagname>` shows where an element starts
    -   A closing tag `</tagname>` shows where it ends
    -   Content goes between them: `<p>A paragraph.</p>`
-   Elements must form a [%g tree "tree" %]: they can nest but cannot overlap
    -   `<ul><li>first</li><li>second</li></ul>` is correct
    -   `<b><i>text</b></i>` is not, because `<i>` opens inside `<b>` but closes after `</b>`
-   The LLM will produce something like `basic_page.html`:

[%inc basic_page.html %]

<div class="callout" markdown="1">

### HTML and Markdown

Markdown is a shorthand notation meant to be readable as plain text and convertible to HTML.
When you write `**bold**` in Markdown, a converter turns it into `<strong>bold</strong>` in HTML.
HTML is what browsers actually understand; Markdown is a shortcut for humans writing documents.
Most web applications, including this tutorial, generate HTML programmatically rather than writing it by hand,
which is why understanding HTML matters even if you rarely type it yourself.

</div>

## Page Structure

*What does every valid HTML page need to have?*

-   Every valid HTML page has four required parts in order:
    -   `<!DOCTYPE html>` on the very first line tells the browser this is modern HTML
    -   An `<html>` element enclosing everything else (the [%g root-element "root element" %])
    -   A `<head>` element containing metadata (information *about* the page, not shown in the window)
    -   A `<body>` element containing the visible content
-   Indentation and blank lines don't change how the browser renders the page: they exist for human readers
-   `<!-- this is a comment -->` adds notes the browser ignores
    -   Comments cannot be nested

## Common Tags

*What are the most common HTML tags I should know?*

-   A short list of tags covers most pages:
    -   `<h1>` through `<h6>` for headings: use them in order, don't skip levels
    -   `<p>` for paragraphs
    -   `<ul>` and `<ol>` for unordered and ordered lists, with `<li>` for each item
    -   `<a>` for links
    -   `<img>` for images
    -   `<em>` and `<strong>` for emphasis and strong emphasis

## Special Characters

*How do I include a less-than sign in HTML without the browser treating it as a tag?*

-   `<` and `>` mark the boundaries of tags, so they cannot appear as-is in text content
-   [%g html-entity "HTML entities" %] are a way to include them and other special characters safely
-   An entity starts with `&`, ends with `;`, and has a name or number in between:
    -   `&lt;` displays as `<`
    -   `&gt;` displays as `>`
    -   `&amp;` displays as `&` (the `&` itself must be escaped because it starts entities)
    -   `&quot;` displays as `"` (useful inside attribute values)
    -   `&copy;` displays as &copy;
    -   `&mdash;` displays as &mdash;
-   In `basic_page.html`, the notes column uses `&gt;` and `&lt;` for weight comparisons,
    and `&amp;` where the text says "volunteers & researchers"
-   A browser that sees `&lt;b&gt;` in text displays `<b>` rather than treating it as a bold tag

## Attributes and Links

*How do I link from one part of a page to another in HTML?*

-   [%g attribute "Attributes" %] appear inside the opening tag and customize how an element behaves: `<tagname name="value">`
-   The `<a>` tag creates a link; its `href` attribute says where the link goes:
    -   A full URL: `<a href="https://example.com">Visit here</a>`
    -   A path relative to the current page: `<a href="./details.html">Details</a>`
    -   An anchor on the current page: `<a href="#recent">Jump to recent sightings</a>`
-   Create an anchor target with an `id` attribute on any element: `<h2 id="recent">Recent Sightings</h2>`
-   The `<img>` tag embeds an image; it is a [%g void-element "void element" %] with no closing tag,
    because it has no text content:
    -   `<img src="map.png" alt="map of sightings">`
    -   The `src` attribute gives the path or URL of the image file
    -   Always include the `alt` attribute, which provides text for screen readers and for when the image cannot load

<div class="callout" markdown="1">

### File Paths vs. URLs

`src="map.png"` is a [%g file-path "file path" %]: the browser looks for `map.png` in the same directory as the HTML file.
You can open the page by double-clicking the file and the image will appear.
`src="https://example.com/map.png"` is a URL: the browser fetches the image from a remote server.
This works in a browser tab, but it requires a network connection and the remote server to be available.
The same distinction applies to `href` in `<link>` and `<a>` tags.
For pages you are developing locally, file paths let you work without running a web server.

</div>

## Tables

*Rewrite the sightings list as a table with one row per sighting and columns for date, species, location, and notes.*

-   A table is made of rows, and each row is made of cells
-   `<table>` wraps the whole table
-   `<tr>` wraps one row
-   `<th>` is a header cell (bold and centered by default)
-   `<td>` is a data cell
-   Rows are listed top to bottom; cells within a row are listed left to right
-   Without CSS a table has no visible borders: the structure is there but the grid lines are not

[%inc table_page.html %]

## Styling with CSS

*Add a stylesheet to the sightings page that sets the font, constrains the page width, and puts borders on the table.*

-   Putting visual styling directly in HTML attributes works but creates problems:
    -   `<h1 align="center">` makes every heading a separate style decision
    -   Hard to keep consistent across a large page, let alone across many pages
-   [%g css "Cascading Style Sheets" %] (CSS) separate content from appearance
-   An [%g internal-style-sheet "internal stylesheet" %] lives in a `<style>` element inside `<head>`
    -   Self-contained: the page looks right when you open the file directly in a browser
-   A CSS [%g css-rule "rule" %] has a [%g css-selector "selector" %] and a block of [%g css-property "properties" %]:

```
selector {
    property-name: value;
    another-property: value;
}
```

-   The selector says which elements the rule applies to
-   `body { font-family: sans-serif; }` sets the font for the entire page
-   `h1 { text-align: center; }` centers every `<h1>` element
-   `th, td { border: 1px solid #cccccc; }` puts a border on both header and data cells
-   `styled_page.html` adds a `<style>` block to `table_page.html` to produce this result:

[%inc styled_page.html %]

<div class="callout" markdown="1">

### Inline Styles

HTML allows styling directly on any element with a `style` attribute:
`<p style="color: red;">Warning.</p>`.
This is called *inline styling*, and it does work, but it's a bad idea for the same reason
copy-pasting is a bad idea.
If you later decide to change that shade of red, you have to hunt down and update every individual element.
A stylesheet keeps all the style decisions in one place so one change affects everything at once.

</div>

## CSS Classes

*How do I make some table cells look different from others using CSS?*

-   Give elements a [%g css-class "class" %] attribute to group them for styling:
    `<td class="note">Female; weight &lt; 150 kg</td>`
-   Target a class in CSS with a dot prefix: `.note { font-style: italic; }`
-   Combine a tag name and a class to be more specific: `td.note { font-style: italic; }`
    (only `<td>` elements with class `note`, not `<p class="note">`)
-   Target a specific element by its unique `id`: `#main-title { font-size: 2em; }`
-   An element can belong to multiple classes: `<td class="note warning">`
-   When two rules could both apply, the more specific one wins
    -   `td.note` overrides `td`, which overrides the browser's built-in defaults
-   In `styled_page.html`, the `note` class styles the notes column in italic gray,
    and `copyright` centers and shrinks the footer line

## Check Understanding

-   See [%b MDN2024 %] for (much) more information

<details markdown="1">
<summary markdown="1">What is wrong with `<p>first <b>bold</p></b>`?</summary>

The `<b>` and `<p>` elements overlap: `<b>` opens inside `<p>` but closes after `</p>`.
HTML elements must be strictly nested, so the correct version is `<p>first <b>bold</b></p>`.

</details>

<details markdown="1">
<summary markdown="1">Why does `<p>Price: 3 < 4 and 5 > 2</p>` cause problems in a browser?</summary>

The browser interprets `<` as the start of a tag and `>` as the end of one,
so it sees `< 4 and 5 >` as a broken tag rather than text.
The correct version is `<p>Price: 3 &lt; 4 and 5 &gt; 2</p>`.

</details>

<details markdown="1">
<summary markdown="1">What is the difference between a class selector (`.highlight`) and an ID selector (`#highlight`)?</summary>

A class selector (`.highlight`) matches every element that has `class="highlight"`,
and any number of elements on the page can share the same class.
An ID selector (`#highlight`) matches the one element with `id="highlight"`,
and each ID must appear at most once per page.
Use classes for styling groups of elements; use IDs for linking to specific spots.

</details>

<details markdown="1">
<summary markdown="1">Why is an internal stylesheet better than inline styles for a page with many elements?</summary>

An internal stylesheet keeps all style decisions in one place.
To change a color, you edit one rule in `<style>` rather than finding every element with `style="..."`.
An external stylesheet (a separate `.css` file included with `<link>`) is even better for sites
with many pages, because one file can style all of them.

</details>

## Exercises

### Add a Navigation Bar

Add an unordered list at the top of `styled_page.html` with links to the `#recent` and `#about` anchors already in the file.
Add CSS rules to the internal stylesheet so the list items appear side by side rather than stacked.

### Color-Code by Species

Edit `styled_page.html` to give each data row a CSS class that matches its species (`canadensis` or `horribilus`).
Add rules to the stylesheet so rows for each species have a different background color.

### Add a Second Page

Create a new file `about.html` in the `htmlcss` directory that describes the
Sasquatch Observation Registry in a paragraph or two.
Add a link from `styled_page.html` to `about.html`, and a link back from `about.html`
to `styled_page.html`.
Give `about.html` the same internal stylesheet as `styled_page.html`.
