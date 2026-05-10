# Claude

This project is an introductory tutorial on web development for
researchers who use LLMs as coding assistants, but have no previous
experience with web development.

## Audience

Learners have completed the first two years of an undergraduate
degree. They have had one semester of programming with Python, and are
comfortable writing one- and two-page programs with loops,
conditionals, lists, dictionaries, and functions, and with creating
objects and calling methods, but have very little experience creating
their own classes. They have seen type annotations, but have never
written their own. They have done one exercise writing tests with
pytest.

Learners have *not* written JavaScript or SQL. They can use basic Unix
shell commands like `cd`, `ls`, and `rm`, but have not written shell
scripts, worked with environment variables, or had to worry about file
permissions. They wrote a little HTML and CSS in high school, but
haven't used it in several years.

Learners do *not* want to become software engineers. They regard
programming as a means to an end.  They care about reproducibility,
and want to be able to have confidence in their results, but are not
going to write complex workflow descriptions or extensive unit test
suites.

Learners frequently use LLM tools like Claude to summarize documents
or write first drafts of emails, to solve homework problems, or in
place of search engines. They do not understand how such tools work,
but would like to. They are nervous that these tools are going to
deskill or eliminate research jobs, and are very concerned about the
social and environmental impact of these tools in general.

## Running Example

-   The running example is a simple web application for managing
    observations of sasquatches in British Columbia. It includes a
    simple synthetic data generator to create datasets for testing.
-   The synthetic data generator is in the `./scripts` directory.
    Building it is *not* part of the tutorial.
-   The finished application stores information in a SQLite database
    with one tables called `sightings`. The table has a sighting ID,
    species name (either "G. canadensis" or "G. horribilus"), sex
    (which may be null), weight (which may be null), color, datetime,
    latitude, and longitude.
-   Users can view all sightings in a single combined table that is
    paginated. They can specify the date range for sightings and only
    view those, or filter by sex, or weight range.
-   Users can add new records to the table using forms. They initially
    do not have to log in to do this. Later versions of the app
    require them to have accounts and log in, and adds columns to the
    table to record who added the observation and when.
-   In later versions of the app, users can view simple charts of
    sightings, including a map.
-   All features are added incrementally and tested along the way.

## Content

-   Each lesson should take one hour to complete, including exercises.
    When in doubt, go slowly.
-   Define new terms using the `%g` shortcode and add definitions to
    `./glossary/index.md`.
-   Each lesson is in its own subdirectory, whose name is a one-word
    descriptive slug. Lessons are included in the `Lessons` section
    of `README.md` in order (see `intro` and `finale` for format).
-   Each lesson has an `index.md` file with an H1 title followed by
    sections with H2 titles.
-   Lesson content in each section is written as point-form lists
    using four-space indentation. *NEVER* put tab characters in files.
    Point-form lists may include sub-lists, but only one level deep.
-   The first H2 in each lesson is `Goals`, which is followed by a
    point-form list of the goals of that lesson. Do not wrap new terms
    in this section in glossary references, but make sure that all new
    terms mentioned here are defined in the lesson.
-   Each H2 title is a short description of the next thing to be added
    to the running example. This is followed by an italicized prompt
    for an LLM that either asks a question or tells the LLM to do the
    next step in the running example. The prompt is given directly,
    without any prefix such as "Ask an LLM", and is not in quotes. The
    prompt is followed by a point-form description of what the LLM
    does, along with excerpts of generated code.
-   Code is put in files in the lesson directory. These files are
    transcluded in the lesson using mccole's `%inc` tag. The shell
    command to run the code (if needed) is put in a `.sh` file in the
    lesson directory, which is also transcluded in the lesson.
-   The penultimate section of each lesson is an H2 titled `Check
    Understanding`. The content underneath this is a series of 3-5
    questions for learners to answer *without* using an LLM. Each
    question is written as `<details markdown="1">`, followed by
    `<summary markdown="1">text of question</summary>` on a line of
    its own, followed by a blank line, followed by a paragraph answer
    and/or snippets of code, followed by a blank line, followed by
    `</details>`.
-   The final section of each lesson is an H2 titled `Exercises`. It
    is followed by 3-5 exercises, each of which has a brief H3 title
    followed by a paragraph describing the goal of the exercise.

## Stack

-   [uv](https://docs.astral.sh/uv/): package and environment management
-   [Alpine.js](https://alpinejs.dev/): browser interaction
-   [HTMX](https://htmx.org/): browser-server communication
-   [Litestar](https://litestar.dev/): server
-   [htpy](https://htpy.dev/): generating HTML
-   [SQLite](https://sqlite.org/): database
-   [pytest](https://docs.pytest.org/): Python testing
-   [Playwright](https://playwright.dev/python/): browser testing (from Python)
-   [ruff](https://astral.sh/ruff): linting Python
-   [ESLint](https://eslint.org/): linting JavaScript
-   [Markuplint](https://markuplint.dev/): linting HTML
-   [taskipy](https://github.com/taskipy/taskipy): task runner

@~/.claude/mccole.md
