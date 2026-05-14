from htpy import a, body, em, h1, h2, head, html, p, style, table, td, th, title, tr

SIGHTINGS = [
    (
        "2024-01-15",
        "G. canadensis",
        "Near Hope, BC",
        "Weight > 200 kg; sex not recorded",
    ),
    ("2024-02-03", "G. horribilus", "Whistler area", "Female; weight < 150 kg"),
    (
        "2024-03-21",
        "G. canadensis",
        "Manning Park",
        'Male; color described as "reddish-brown"',
    ),
]

# mccole:css-definition
# CSS as a plain string; htpy places it inside <style> without escaping
CSS = """
    body { font-family: sans-serif; max-width: 40em; margin: 1em auto; padding: 0 1em; }
    h1 { text-align: center; color: #333333; }
    h2 { border-bottom: 1px solid #cccccc; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #cccccc; padding: 0.4em 0.8em; text-align: left; }
    th { background-color: #eeeeee; }
    .note { font-style: italic; color: #666666; }
    .copyright { text-align: center; font-size: 0.85em; color: #999999; }
"""

page = html(lang="en")[
    head[
        title["Sasquatch Sightings"],
        style[CSS],
    ],
# mccole:/css-definition
# mccole:styled-rows
    body[
        h1["Sasquatch Sightings in British Columbia"],
        p[
            "This page records recent sightings of ",
            em["Gigantopithecus canadensis"],
            " and ",
            em["G. horribilus"],
            " in British Columbia. "
            "Data was collected by volunteers & researchers between January and March 2024.",
        ],
        h2(id="recent")["Recent Sightings"],
        table[
            tr[th["Date"], th["Species"], th["Location"], th["Notes"]],
            [
                tr[td[date], td[species], td[location], td(class_="note")[notes]]
                for date, species, location, notes in SIGHTINGS
            ],
        ],
        h2(id="about")["About This Project"],
        p[
            "The Sasquatch Observation Registry collects verified sightings "
            "from trained volunteers across British Columbia. "
            "Jump back to ",
            a(href="#recent")["recent sightings"],
            " or visit ",
            a(href="https://example.com/sasquatch")["the project website"],
            ".",
        ],
        p(class_="copyright")["\u00a9 2024 Sasquatch Research Institute"],
    ],
]

print(str(page))
# mccole:/styled-rows
