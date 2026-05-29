import csv
from abc import ABC, abstractmethod

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


class StorageBackend(ABC):
    """Abstraction for saving and loading visitor rows."""

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def save_all(self, visitors):
        pass

    @abstractmethod
    def append_record(self, visitor):
        pass


class CSVStorage(StorageBackend):
    """Concrete storage class that persists records in a CSV file."""

    def __init__(self, file_name=FILE_NAME, fieldnames=None):
        self._file_name = file_name
        self._fieldnames = fieldnames or FIELDNAMES

    def _get_date_from_time_in(self, row):
        time_in = row.get("time_in", "")
        return time_in[:10] if len(time_in) >= 10 else ""

    def _normalize_row(self, row):
        if hasattr(row, "to_dict"):
            row = row.to_dict()

        normalized = {}

        for field in self._fieldnames:
            normalized[field] = row.get(field, "")

        if not normalized["date"]:
            normalized["date"] = self._get_date_from_time_in(normalized)

        return normalized

    def create_file_if_missing(self):
        try:
            with open(self._file_name, "x", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self._fieldnames)
                writer.writeheader()
        except FileExistsError:
            pass

    def load_data(self):
        visitors = []
        self.create_file_if_missing()

        with open(self._file_name, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            needs_migration = reader.fieldnames != self._fieldnames

            for row in reader:
                visitors.append(self._normalize_row(row))

        if needs_migration:
            self.save_all(visitors)

        return visitors

    def save_all(self, visitors):
        with open(self._file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self._fieldnames)
            writer.writeheader()

            for visitor in visitors:
                writer.writerow(self._normalize_row(visitor))

    def append_record(self, visitor):
        self.create_file_if_missing()

        with open(self._file_name, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self._fieldnames)
            writer.writerow(self._normalize_row(visitor))


_default_storage = CSVStorage()


def create_file_if_missing():
    """Create the CSV file with headers if it does not exist yet."""
    _default_storage.create_file_if_missing()


def load_data():
    """Load all visitor records from CSV."""
    return _default_storage.load_data()


def save_all(visitors):
    """Rewrite the CSV file after a record is updated."""
    _default_storage.save_all(visitors)


def append_record(visitor):
    """Append a single visitor record to the CSV file."""
    _default_storage.append_record(visitor)
