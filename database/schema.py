CREATE_TABLE = """
    create table sightings (
        id integer primary key,
        species text not null,
        sex text,
        weight real,
        color text not null,
        datetime text not null,
        latitude real not null,
        longitude real not null
    )
"""
