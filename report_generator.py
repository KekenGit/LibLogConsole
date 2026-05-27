from datetime import datetime
import os
from liblog_function import get_visitors

REPORT_FOLDER = "reports"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_datetime(value):
    return datetime.strptime(value, DATETIME_FORMAT)


def is_today(visitor, today):
    return visitor.get("date") == today


def format_peak_hour(hour):
    if hour is None:
        return "N/A"

    return f"{hour:02d}:00 - {hour:02d}:59"


def get_peak_hour(visitors):
    hourly_counts = {}

    for visitor in visitors:
        try:
            hour = parse_datetime(visitor["time_in"]).hour
            hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
        except (KeyError, ValueError):
            pass

    if not hourly_counts:
        return None

    return max(hourly_counts, key=hourly_counts.get)


def generate_report():

    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    today = datetime.now().strftime("%Y-%m-%d")
    visitors = [
        visitor
        for visitor in get_visitors()
        if is_today(visitor, today)
    ]

    total = len(visitors)
    inside = len([
        visitor
        for visitor in visitors
        if visitor.get("time_out", "") == ""
    ])
    completed = total - inside

    durations = []

    for visitor in visitors:
        if visitor.get("time_out", ""):
            try:
                time_in = parse_datetime(visitor["time_in"])
                time_out = parse_datetime(visitor["time_out"])
                durations.append((time_out - time_in).total_seconds())
            except (KeyError, ValueError):
                pass

    avg_duration = sum(durations) / len(durations) if durations else 0
    peak_hour = get_peak_hour(visitors)

    report_text = f"""
===== LIBLOG DAILY REPORT =====
Date: {today}

Total Check-ins: {total}
Peak Hour: {format_peak_hour(peak_hour)}
Average Visit Duration: {avg_duration / 60:.2f} minutes
Visitors Still Inside: {inside}
Completed Visits: {completed}
"""

    filename = os.path.join(REPORT_FOLDER, f"report_{today}.txt")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report_text)

    print("\nReport generated successfully!")
    print("Saved as:", filename)
