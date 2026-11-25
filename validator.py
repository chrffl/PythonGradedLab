import re
import math
from datetime import datetime

FLIGHT_ID_RE = re.compile(r"^[A-Za-z0-9]{2,8}$")
AIRPORT_CODE_RE = re.compile(r"^[A-Z]{3}$")
DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")

def parse_datetime(text: str):
    if not DATETIME_RE.match(text):
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d %H:%M")
    except ValueError:
        return None

def load_airports(path: str) -> set[str]:
    airports = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            airports.add(line)
    return airports


def validate_row(fields: list[str], airports: set[str]) -> str | None:
    if len(fields) != 6:
        return "WRONG_FIELD_COUNT"

    flight_id, origin, destination, departure, arrival, price = [f.strip() for f in fields]

    if not flight_id or not origin or not destination or not departure or not arrival or not price:
        return "MISSING_FIELD"

    if not FLIGHT_ID_RE.match(flight_id):
        return "INVALID_FLIGHT_ID"


def to_record(fields: list[str]) -> dict:
    """Turn a valid row into a flight record dictionary.

    Keys: flight_id, origin, destination, departure_datetime,
    arrival_datetime (stripped strings) and price (float).
    """
    raise NotImplementedError
