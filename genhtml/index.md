# Generating HTML

## Goals

-   Understand different ways to generate HTML from Python and when each is appropriate.
-   Use htpy to build an HTML page by composing Python expressions.
-   Pass attributes to HTML elements using keyword arguments.
-   Rely on htpy's automatic escaping instead of writing HTML entities by hand.
-   Build a table from data using a list comprehension.

## Three Ways to Do It

*What are the main ways to generate HTML from Python, and what are the tradeoffs?*

-   Every web application has to turn data into HTML
-   Method 1: f-strings and concatenation
    -   Build HTML the same way you'd build any string, using `+` or f-strings:
        `page = f"<html><head><title>{title}</title></head><body><ul>{row}</ul></body></html>"`
    -   Works for tiny examples but breaks down quickly
    -   The `>` in `Weight > 200 kg` confuses the browser unless you replace it with `&gt;` yourself,
    -   Nested f-strings have no structure, so three levels deep the code becomes unreadable
-   Method 2: [%g template-engine "template engines" %] like [Jinja][jinja]
    -   Write HTML files with placeholders that get filled in at runtime:
        `{% for sighting in sightings %}<li>{{ sighting.notes }}</li>{% endfor %}`
    -   Auto-escapes values by default, so `>` becomes `&gt;` without any effort on your part
    -   Cost: you now maintain two kinds of files (Python and HTML templates) and must learn
        a second mini-language for the template logic
-   Method 3: [htpy][htpy]
    -   Instead of HTML with Python holes, write Python that produces HTML
    -   Every tag is a Python object whose children go inside square brackets

*Show an example of how htpy works.*

```python
from htpy import ul, li
print(str(ul[li["item one"], li["item two"]]))
```

```
<ul><li>item one</li><li>item two</li></ul>
```

-   htpy escapes special characters automatically, so you never write `&gt;` or `&amp;` by hand
-   The HTML structure is visible in the indentation of the Python code
-   Because it is all Python you can use loops, functions, and variables exactly as you would anywhere else

## Building the Basic Page

*Rewrite `htmlcss/basic_page.html` as a Python script using htpy.*

-   Import each tag you need from `htpy` at the top of the file
-   Build the page by nesting elements inside each other using `[...]`
-   Call `print(str(page))` at the end to write the HTML to the terminal

*How do I add an `id` attribute to an element in htpy?*

-   Pass attributes as [%g keyword-argument "keyword arguments" %]
    when you call the element: `h2(id="recent")["Recent Sightings"]`
-   The `href` attribute on a link works the same way: `a(href="#recent")["jump here"]`
-   htpy escapes `&`, `<`, and `>` in text content automatically,
    so `"volunteers & researchers"` becomes `volunteers &amp; researchers` in the output

[%inc basic_page.py %]

## Building the Table Page

*Rewrite `htmlcss/table_page.html` as a Python script using htpy. Store the sightings data in a list of tuples.*

-   Import `table`, `tr`, `th`, and `td` from `htpy`
-   Put the data in a list of tuples near the top of the file so it is easy to find and change
-   Use a [%g list-comprehension "list comprehension" %] to build the data rows:
    `[tr[td[date], td[species], ...] for date, species, ... in SIGHTINGS]`
-   htpy accepts a list anywhere it accepts a single child,
    so you can pass the comprehension directly inside `table[...]`

[%inc table_page.py %]

## Adding a Stylesheet

*Rewrite `htmlcss/styled_page.html` as a Python script using htpy. Include the CSS stylesheet and apply the `note` and `copyright` classes.*

-   Import `style` from `htpy` and put your CSS inside it as a plain Python string
-   htpy does *not* escape the contents of `<style>` elements,
    because CSS uses `{`, `}`, and `:` which are not HTML-special characters
-   The `class` attribute is a reserved word in Python, so htpy uses `class_` instead:
    `td(class_="note")[notes]`
-   Apply `class_="copyright"` to the copyright paragraph the same way

[%inc styled_page.py mark=css-definition %]

[%inc styled_page.py mark=styled-rows %]

## Check Understanding

<details markdown="1">
<summary markdown="1">What does htpy use instead of `class="..."` as a keyword argument, and why?</summary>

htpy uses `class_` (with a trailing underscore) because `class` is a reserved word in Python---it
is used to define new classes and cannot appear as a function argument name.
Adding an underscore is a standard Python convention for working around name conflicts with built-in keywords.

</details>

<details markdown="1">
<summary markdown="1">You write `td["Weight > 200 kg"]` in htpy. What does the browser receive, and why?</summary>

The browser receives `<td>Weight &gt; 200 kg</td>`.
htpy automatically escapes `>` as `&gt;` in text content so the browser does not mistake it for
the start of a closing tag.
This happens for `<` (becomes `&lt;`) and `&` (becomes `&amp;`) as well.

</details>

<details markdown="1">
<summary markdown="1">The script below raises a `TypeError`. What is wrong and how do you fix it?</summary>

```python
from htpy import ul, li
page = ul(li["first"], li["second"])
print(str(page))
```

The round brackets `(...)` pass arguments to configure the element's attributes.
To give an element its children, use square brackets `[...]`.
The fix is:

```python
page = ul[li["first"], li["second"]]
```

</details>

<details markdown="1">
<summary markdown="1">What is the advantage of storing sightings data in a list of tuples (as in `table_page.py`) rather than hard-coding the table rows directly in the htpy expression?</summary>

Separating data from structure means you can change one without touching the other.
If the sightings list comes from a database or a file later in the tutorial,
you only need to change where `SIGHTINGS` comes from, not the code that builds the table.
It also makes the table-building code shorter and easier to read.

</details>

<details markdown="1">
<summary markdown="1">A classmate writes this to center a heading: `h1(style="text-align: center")["Title"]`.
It works, but is it a good idea? Why or why not?</summary>

It works for a single heading, but it is the same problem as inline styles in HTML:
if you later decide to change the alignment, you have to find and edit every element that has the style attribute.
A better approach is to define `.centered { text-align: center; }` in the CSS string and apply it with
`h1(class_="centered")["Title"]`, so one change in the CSS affects every element that uses the class.

</details>

<details markdown="1">
<summary markdown="1">The `SIGHTINGS` list in `table_page.py` contains the string `'Male; color described as "reddish-brown"'`. The original `table_page.html` uses `&quot;` for those double-quotes. What does htpy put in the output---`&quot;`, `&#34;`, the literal `"`, or something else?</summary>

htpy outputs `&#34;`, the numeric character reference for `"`.
The original HTML file used `&quot;`, which is the named entity for the same character.
Both are valid HTML and display identically in a browser.
Double-quotes do not actually need escaping in text content (only inside attribute values),
but htpy escapes them anyway using the numeric form.
You can verify this yourself by running `python table_page.py` and searching the output.

</details>

See [%b htpy2025 %] for the full htpy documentation and [%b mdn-html2024 %] for reference on HTML elements and attributes.

## Exercises

### Add a Caption

HTML tables support an optional `<caption>` element placed immediately after the opening `<table>` tag.
Import `caption` from `htpy` and add a caption to the table in `table_page.py`.
Add a CSS rule to `styled_page.py` that centers the caption and makes it italic.

### Generate the List from Data

Rewrite `basic_page.py` so the three sightings in the `<ul>` are generated from a list of tuples,
using the same pattern as `table_page.py`.
Verify that the HTML output is identical to what the original script produced.

### Add a Navigation Bar

Add an unordered list at the top of the `<body>` in `styled_page.py` with links to
the `#recent` and `#about` anchors.
Add a CSS rule to the stylesheet string so the list items appear side by side rather than stacked.

### Extract a Page Builder Function

Define a Python function `make_page(heading, rows)` that returns a complete `html[...]` element
given a heading string and a list of row tuples.
Call it from a short `__main__` block to produce the same output as `styled_page.py`.

### Color-Code by Species

Edit `styled_page.py` so each data row has a CSS class that matches its species
(`canadensis` or `horribilus`).
Add CSS rules to the stylesheet string so each species has a different background color.
