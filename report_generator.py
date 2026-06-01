from abc import ABC, abstractmethod
from datetime import datetime
import os
from liblog_function import get_visitors
from visitor_record import DATETIME_FORMAT

REPORT_FOLDER = "reports"


class Report(ABC):
    """Abstraction for any report the system can generate."""

    @abstractmethod
    def build(self):
        pass


class DailyReport(Report):
    """Concrete report for one day of library visitor activity."""

    def __init__(self, visitors, report_date):
        self._visitors = visitors
        self._report_date = report_date

    def get_daily_visitors(self):
        return [
            visitor
            for visitor in self._visitors
            if is_today(visitor, self._report_date)
        ]

    def build(self):
        visitors = self.get_daily_visitors()

        total = len(visitors)
        inside = len([
            visitor
            for visitor in visitors
            if visitor.is_active_on(self._report_date)
        ])
        completed = total - inside

        durations = []

        for visitor in visitors:
            if visitor.time_out:
                try:
                    time_in = parse_datetime(visitor.time_in)
                    time_out = parse_datetime(visitor.time_out)
                    durations.append((time_out - time_in).total_seconds())
                except ValueError:
                    pass

        avg_duration = sum(durations) / len(durations) if durations else 0
        peak_hour = get_peak_hour(visitors)

        return f"""
===== LIBLOG DAILY REPORT =====
Date: {self._report_date}

Total Check-ins: {total}
Peak Hour: {format_peak_hour(peak_hour)}
Average Visit Duration: {avg_duration / 60:.2f} minutes
Visitors Still Inside: {inside}
Completed Visits: {completed}
"""


def parse_datetime(value):
    return datetime.strptime(value, DATETIME_FORMAT)


def is_today(visitor, today):
    return visitor.is_for_date(today)


def format_peak_hour(hour):
    if hour is None:
        return "N/A"

    return f"{hour:02d}:00 - {hour:02d}:59"


def get_peak_hour(visitors):
    hourly_counts = {}

    for visitor in visitors:
        try:
            hour = parse_datetime(visitor.time_in).hour
            hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
        except ValueError:
            pass

    if not hourly_counts:
        return None

    return max(hourly_counts, key=hourly_counts.get)


def save_report(report, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report.build())


def generate_report():

    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    today = datetime.now().strftime("%Y-%m-%d")
    report = DailyReport(get_visitors(), today)

    filename = os.path.join(REPORT_FOLDER, f"report_{today}.txt")
    save_report(report, filename)

    print("\nReport generated successfully!")
    print("Saved as:", filename)
