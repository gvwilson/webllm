"""Generate synthetic sasquatch sighting data for testing."""

import argparse
from datetime import datetime, timedelta
import csv
import random
import sys


# Default random seed chosen arbitrarily for reproducibility
DEFAULT_SEED = 7493418

# Default number of records to generate
DEFAULT_COUNT = 100

# Species observed in British Columbia
SPECIES = ["G. canadensis", "G. horribilus"]

# Observed coat colors
COLORS = ["black", "dark brown", "brown", "gray", "reddish-brown"]

# Probability that sex is recorded (observers sometimes can't tell)
PROB_SEX_RECORDED = 0.75

# Probability that weight is recorded (rarely measured directly)
PROB_WEIGHT_RECORDED = 0.40

# Fraction of sightings that are juveniles
JUVENILE_FRACTION = 0.30

# Weight ranges in kg, based on gorilla data as proxy
# Adult male: 140-180 kg, adult female: 70-100 kg, juvenile: 20-60 kg
WEIGHT_RANGE_ADULT_MALE = (140.0, 180.0)
WEIGHT_RANGE_ADULT_FEMALE = (70.0, 100.0)
WEIGHT_RANGE_JUVENILE = (20.0, 60.0)

# Rocky Mountains of British Columbia bounding box (approximate)
LAT_MIN = 49.0
LAT_MAX = 58.0
LON_MIN = -125.0
LON_MAX = -115.0

# Date range for sightings
DATE_START = datetime(2010, 1, 1)
DATE_END = datetime(2025, 12, 31)
DATE_RANGE_DAYS = (DATE_END - DATE_START).days


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic sasquatch sighting data."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help=f"random number generator seed (default: {DEFAULT_SEED})",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_COUNT,
        help=f"number of sightings to generate (default: {DEFAULT_COUNT})",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="path to output CSV file (default: print to stdout)",
    )
    args = parser.parse_args()

    rng = random.Random(args.seed)
    sightings = [generate_sighting(rng, i + 1) for i in range(args.count)]

    fieldnames = [
        "sighting_id",
        "species",
        "sex",
        "weight",
        "color",
        "datetime",
        "latitude",
        "longitude",
    ]

    if args.output:
        out = open(args.output, "w", newline="")
    else:
        out = sys.stdout

    writer = csv.DictWriter(out, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(sightings)

    if args.output:
        out.close()


def generate_sighting(rng, sighting_id):
    """Generate a single sighting record."""
    species = rng.choice(SPECIES)
    is_juvenile = rng.random() < JUVENILE_FRACTION

    if is_juvenile:
        sex = rng.choice(["male", "female", None])
        weight_range = WEIGHT_RANGE_JUVENILE
    else:
        sex = rng.choice(["male", "female"])
        weight_range = (
            WEIGHT_RANGE_ADULT_MALE if sex == "male" else WEIGHT_RANGE_ADULT_FEMALE
        )

    if rng.random() > PROB_SEX_RECORDED:
        sex = None

    weight = None
    if rng.random() < PROB_WEIGHT_RECORDED:
        weight = round(rng.uniform(*weight_range), 1)

    color = rng.choice(COLORS)
    sighting_date = DATE_START + timedelta(days=rng.randint(0, DATE_RANGE_DAYS))
    hour = rng.randint(0, 23)
    minute = rng.randint(0, 59)
    dt = sighting_date.replace(hour=hour, minute=minute, second=0)

    lat = round(rng.uniform(LAT_MIN, LAT_MAX), 6)
    lon = round(rng.uniform(LON_MIN, LON_MAX), 6)

    return {
        "sighting_id": sighting_id,
        "species": species,
        "sex": sex if sex is not None else "",
        "weight": weight if weight is not None else "",
        "color": color,
        "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "latitude": lat,
        "longitude": lon,
    }


if __name__ == "__main__":
    main()
