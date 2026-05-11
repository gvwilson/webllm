# Log: 2026-05-10-23-38 generate-data-script

## Prompts

1. Create a `scripts/` directory and add `scripts/generate_data.py` that generates a CSV file
   of sasquatch observations with argparse, configurable seed (default 7493418), configurable
   output path, gorilla-appropriate weights, Rocky Mountains BC coordinates, and juveniles.

## Actions

-   Created `scripts/` directory.
-   Created `scripts/generate_data.py` with:
    -   `--seed` argument (default 7493418) using `random.Random` for reproducibility
    -   `--count` argument (default 100)
    -   `--output` argument (default stdout)
    -   Species: "G. canadensis" or "G. horribilus"
    -   Sex: male/female/null (75% chance of being recorded; juveniles may be null)
    -   Weight: null 60% of the time; ranges from gorilla data (adult male 140-180 kg,
        adult female 70-100 kg, juvenile 20-60 kg)
    -   Color: black, dark brown, brown, gray, reddish-brown
    -   Datetime: random timestamp between 2000-01-01 and 2025-12-31
    -   Latitude: 49.0-58.0 N (Rocky Mountains of BC)
    -   Longitude: 115.0-125.0 W (Rocky Mountains of BC)
    -   ~20% of sightings are juveniles
