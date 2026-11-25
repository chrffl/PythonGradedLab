import csv
import os

from validator import to_record, validate_row

#THAT part of the code was done with the help of CHAT GPT
def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    records = []
    errors = []
    seen = set()

    for path in paths:
        file_name = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            for line_number, raw_line in enumerate(f, start=1):
                if line_number == 1:
                    continue
                #THAT part of the code was done with the help of CHAT GPT

                content = raw_line.strip()
                if not content or content.startswith("#"):
                    continue

                fields = next(csv.reader([content]))
                code = validate_row(fields, airports)
                if code is not None:
                    errors.append(f"{file_name}:{line_number}: {code} | {content}")
                    continue

                record = to_record(fields)
                key = (record["flight_id"], record["departure_datetime"])
                if key in seen:
                    errors.append(f"{file_name}:{line_number}: DUPLICATE_FLIGHT | {content}")
                    continue

                seen.add(key)
                records.append(record)

    return records, errors