LABELS = {
    "id": "ID",
    "species": "Species",
    "sex": "Sex",
    "weight": "Weight (kg)",
    "color": "Color",
    "datetime": "Date/Time",
    "latitude": "Latitude",
    "longitude": "Longitude",
}
HEADERS = list(LABELS.values())
KEYS = list(LABELS.keys())


def fmt(v):
    return str(v) if v is not None else ""
