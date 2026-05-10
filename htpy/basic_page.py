from htpy import a, body, em, h1, h2, head, html, li, p, title, ul

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
        ul[
            li["2024-01-15: ", em["G. canadensis"], " near Hope, BC. Weight > 200 kg."],
            li["2024-02-03: ", em["G. horribilus"], " near Whistler. Female; weight < 150 kg."],
            li["2024-03-21: ", em["G. canadensis"], " in Manning Park. Color: \"reddish-brown\"."],
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
