from htpy import a, body, em, h1, h2, head, html, p, table, td, th, title, tr

SIGHTINGS = [
    ("2024-01-15", "G. canadensis", "Near Hope, BC", "Weight > 200 kg; sex not recorded"),
    ("2024-02-03", "G. horribilus", "Whistler area", "Female; weight < 150 kg"),
    ("2024-03-21", "G. canadensis", "Manning Park", 'Male; color described as "reddish-brown"'),
]

page = html(lang="en")[
    head[title["Sasquatch Sightings"]],
    body[
        h1["Sasquatch Sightings in British Columbia"],
        p[
            "This page records recent sightings of ",
            em["Gigantopithecus canadensis"],
            " and ",
            em["G. horribilus"],
            " in British Columbia. "
            "Data was collected by volunteers & researchers in early 2024.",
        ],
        h2(id="recent")["Recent Sightings"],
        table[
            tr[th["Date"], th["Species"], th["Location"], th["Notes"]],
            [tr[td[date], td[species], td[location], td[notes]]
             for date, species, location, notes in SIGHTINGS],
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
        p["\u00a9 2024 Sasquatch Research Institute"],
    ],
]

print(str(page))
