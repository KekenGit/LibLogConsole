from datetime import datetime
import os
from csv_handler import load_data, save_all, append_record

MAX_CAPACITY = 20
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

visitors = load_data()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def get_today():
    return datetime.now().strftime("%Y-%m-%d")


def is_today(visitor):
    return visitor.get("date") == get_today()


def get_current_occupancy():
    return len([
        visitor
        for visitor in visitors
        if is_today(visitor) and visitor.get("time_out", "") == ""
    ])


def input_required(label):
    while True:
        value = input(label).strip()

        if value:
            return value

        print("This field is required. Please try again.")


# =========================
# FEATURE 1: CHECK IN
# =========================
def check_in():

    clear_screen()
    print("===== CHECK-IN =====")

    if get_current_occupancy() >= MAX_CAPACITY:
        print("\nLibrary is already at full capacity!")
        return

    name = input_required("Full Name: ")
    reason = input_required("Reason of Visit: ")
    address = input_required("Exact Location / Address: ")
    school = input_required("School: ")
    signature = input_required("Signature (typed name): ")

    now = datetime.now()
    visit_date = now.strftime("%Y-%m-%d")
    time_in = now.strftime(DATETIME_FORMAT)

    visitor = {
        "date": visit_date,
        "name": name,
        "reason": reason,
        "address": address,
        "school": school,
        "signature": signature,
        "time_in": time_in,
        "time_out": "",
        "duration": "",
    }

    visitors.append(visitor)
    append_record(visitor)

    print("\nCheck-in successful!")
    print("Date:", visit_date)
    print("Time In:", time_in)
    print("Current Occupancy:", get_current_occupancy())


# =========================
# FEATURE 2: CHECK OUT
# =========================
def check_out():

    clear_screen()
    print("===== CHECK-OUT =====")

    name = input_required("Enter Name: ")

    for visitor in visitors:
        if (
            visitor["name"].lower() == name.lower()
            and is_today(visitor)
            and visitor.get("time_out", "") == ""
        ):
            time_out = datetime.now()
            time_in = datetime.strptime(visitor["time_in"], DATETIME_FORMAT)
            duration = time_out - time_in

            visitor["time_out"] = time_out.strftime(DATETIME_FORMAT)
            visitor["duration"] = str(duration)

            save_all(visitors)

            print("\nCheck-out successful!")
            print("Time Out:", visitor["time_out"])
            print("Duration:", duration)
            print("Current Occupancy:", get_current_occupancy())
            return

    print("Visitor not found or already checked out today!")


# =========================
# FEATURE 3: LIVE OCCUPANCY
# =========================
def view_occupancy():

    clear_screen()

    inside = get_current_occupancy()
    percent = (inside / MAX_CAPACITY) * 100

    print("===== OCCUPANCY =====")
    print("Current Occupancy:", inside)
    print("Maximum Capacity:", MAX_CAPACITY)
    print(f"Percentage Full: {percent:.2f}%")

    if inside >= MAX_CAPACITY:
        print("WARNING: Library is FULL!")
    elif inside >= MAX_CAPACITY * 0.8:
        print("WARNING: Library is NEAR CAPACITY!")
    else:
        print("Library occupancy is normal.")


# =========================
# HELPER FUNCTIONS
# =========================
def get_visitors():
    return visitors


def get_max_capacity():
    return MAX_CAPACITY
