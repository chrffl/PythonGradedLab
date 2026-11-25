import argparse
import json
import logging
import os
import sys
from datetime import datetime

from csv_loader import parse_files
from query import run_queries
from validator import load_airports

# TODO: fill in your details: plain ASCII, no spaces or underscores.
STUDENT_ID = "260ADB159"
FIRST_NAME = "Polina"
LAST_NAME = "Pavlova"


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description="Flight Schedule Parser and Query Tool")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i", dest="input_file")
    source.add_argument("-d", dest="input_dir")
    source.add_argument("-j", dest="json_db")
    parser.add_argument("-a", dest="airports")
    parser.add_argument("-o", dest="output")
    parser.add_argument("-q", dest="queries")
    parser.add_argument("-r", dest="response_dir", default=".")

    args = parser.parse_args(argv)

    if (args.input_file or args.input_dir) and not args.airports:
        parser.error("-a is required with -i or -d")

    if args.json_db and args.output is not None:
        parser.error("-o cannot be used with -j")

    return args

def read_csv_files(paths, airports):
    return parse_files(paths, airports)


def save_database(records, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

#Using CHATGPT
def write_errors(messages, log_path):
    logger = logging.getLogger("flight_parser")
    logger.setLevel(logging.WARNING)
    logger.propagate = False

    handler = logging.FileHandler(
        log_path, mode="w", encoding="utf-8"
    )

    try:
        handler.setLevel(logging.WARNING)

        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))

        logger.addHandler(handler)

        for message in messages:
            logger.warning(message)

    finally:
        logger.removeHandler(handler)
        handler.close()
#Using CHATGPT

def load_database(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array")
    return data

def process_queries(db, queries_path, response_dir):
    with open(queries_path, encoding="utf-8") as f:
        queries = json.load(f)

    if not isinstance(queries, (dict, list)):
        raise ValueError(f"{queries_path} must contain a query object or a list of query objects")

    responses = run_queries(db, queries)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_{timestamp}.json"
    with open(os.path.join(response_dir, filename), "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=2)


if __name__ == "__main__":
    sys.exit(main())
