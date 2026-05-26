import csv

FILE_NAME = "liblog_data.csv"

FIELDNAMES = [
    "date",
    "name",
    "reason",
    "address",
    "school",
    "signature",
    "time_in",
    "time_out",
    "duration",
]


def _get_date_from_time_in(row):
    time_in = row.get("time_in", "")
    return time_in[:10] if len(time_in) >= 10 else ""


def _normalize_row(row):
    """Make old and new CSV rows use the same fields."""
    normalized = {}

    for field in FIELDNAMES:
        normalized[field] = row.get(field, "")

    if not normalized["date"]:
        normalized["date"] = _get_date_from_time_in(normalized)

    return normalized


def create_file_if_missing():
    """Create the CSV file with headers if it does not exist yet."""
    try:
        with open(FILE_NAME, "x", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
    except FileExistsError:
        pass


def load_data():
    """Load all visitor records from CSV."""
    visitors = []
    create_file_if_missing()

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        needs_migration = reader.fieldnames != FIELDNAMES

        for row in reader:
            visitors.append(_normalize_row(row))

    if needs_migration:
        save_all(visitors)

    return visitors


def save_all(visitors):
    """Rewrite the CSV file after a record is updated."""
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for visitor in visitors:
            writer.writerow(_normalize_row(visitor))


def append_record(visitor):
    """Append a single visitor record to the CSV file."""
    create_file_if_missing()

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(_normalize_row(visitor))
