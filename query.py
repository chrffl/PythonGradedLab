from validator import parse_datetime

ALLOWED_KEYS = {
    "flight_id", "origin", "destination", "departure_datetime", "arrival_datetime",
    "price", "min_price", "sort_by", "order", "limit",
}
SORT_KEYS = {"flight_id", "origin", "destination", "departure_datetime", "arrival_datetime", "price"}


def is_valid_query(query: dict) -> bool:
    if not isinstance(query, dict):
        return False

    for key in query:
        if key not in ALLOWED_KEYS:
            return False

    for key in ("flight_id", "origin", "destination"):
        if key in query and not isinstance(query[key], str):
            return False

    for key in ("departure_datetime", "arrival_datetime"):
        if key in query:
            value = query[key]
            if not isinstance(value, str) or parse_datetime(value) is None:
                return False

    for key in ("price", "min_price"):
        if key in query:
            value = query[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return False

    if "limit" in query:
        value = query["limit"]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            return False

    if "sort_by" in query and query["sort_by"] not in SORT_KEYS:
        return False

    if "order" in query:
        if query["order"] not in ("asc", "desc"):
            return False
        if "sort_by" not in query:
            return False

    return True


def flight_matches(flight: dict, query: dict) -> bool:
    if "flight_id" in query and flight["flight_id"] != query["flight_id"]:
        return False
    if "origin" in query and flight["origin"] != query["origin"]:
        return False
    if "destination" in query and flight["destination"] != query["destination"]:
        return False
    if "departure_datetime" in query and flight["departure_datetime"] < query["departure_datetime"]:
        return False
    if "arrival_datetime" in query and flight["arrival_datetime"] > query["arrival_datetime"]:
        return False
    if "price" in query and flight["price"] > query["price"]:
        return False
    if "min_price" in query and flight["price"] < query["min_price"]:
        return False
    return True


def run_query(db: list[dict], query: dict) -> dict:
    if not is_valid_query(query):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}

    matches = [flight for flight in db if flight_matches(flight, query)]

    sort_by = query.get("sort_by")
    if sort_by is not None:
        matches = sorted(matches, key=lambda flight: flight[sort_by], reverse=query.get("order") == "desc")

    limit = query.get("limit")
    if limit is not None:
        matches = matches[:limit]

    return {"query": query, "matches": matches}


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    if isinstance(queries, dict):
        queries = [queries]
    return [run_query(db, query) for query in queries]