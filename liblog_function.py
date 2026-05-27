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


def get_active_visitors():
    return [
        visitor
        for visitor in visitors
        if is_today(visitor) and visitor.get("time_out", "") == ""
    ]


def has_active_visitor(name):
    return any(
        visitor["name"].lower() == name.lower()
        for visitor in get_active_visitors()
    )


def input_required(label, allow_cancel=False):
    while True:
        value = input(label).strip()

        if allow_cancel and value == "0":
            return None

        if value:
            return value

        print("This field is required. Please try again.")


def input_check_in_field(label):
    return input_required(label, allow_cancel=True)


def cancel_check_in_if_needed(value):
    if value is None:
        print("\nCheck-in cancelled.")
        return True

    return False


# =========================
# FEATURE 1: CHECK IN
# =========================
def check_in():

    clear_screen()
    print("===== CHECK-IN =====")
    print("Enter 0 anytime to cancel check-in.")

    if get_current_occupancy() >= MAX_CAPACITY:
        print("\nLibrary is already at full capacity!")
        return

    name = input_check_in_field("Full Name: ")

    if cancel_check_in_if_needed(name):
        return

    if has_active_visitor(name):
        print("\nThis visitor is already checked in.")
        print("Please check out the existing record before checking in again.")
        return

    reason = input_check_in_field("Reason of Visit: ")
    if cancel_check_in_if_needed(reason):
        return

    address = input_check_in_field("Exact Location / Address: ")
    if cancel_check_in_if_needed(address):
        return

    school = input_check_in_field("School: ")
    if cancel_check_in_if_needed(school):
        return

    signature = input_check_in_field("Signature (typed name): ")
    if cancel_check_in_if_needed(signature):
        return

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
def display_active_visitors(active_visitors):
    print("\nVisitors Currently Inside:")
    print("--------------------------")

    for index, visitor in enumerate(active_visitors, start=1):
        print(f"{index}. {visitor['name']}")

    print("0. Cancel check-out")
    print("--------------------------")


def select_active_visitor(active_visitors):
    while True:
        choice = input_required("Enter your choice: ")

        if choice == "0":
            return None

        if choice.isdigit():
            selected_index = int(choice) - 1

            if 0 <= selected_index < len(active_visitors):
                return active_visitors[selected_index]

        print("Invalid selection. Please choose a number from the list.")


def complete_check_out(visitor):
    time_out = datetime.now()
    time_in = datetime.strptime(visitor["time_in"], DATETIME_FORMAT)
    duration = time_out - time_in

    visitor["time_out"] = time_out.strftime(DATETIME_FORMAT)
    visitor["duration"] = str(duration)

    save_all(visitors)

    print("\nCheck-out successful!")
    print("Name:", visitor["name"])
    print("Time Out:", visitor["time_out"])
    print("Duration:", duration)
    print("Current Occupancy:", get_current_occupancy())


def check_out():

    clear_screen()
    print("===== CHECK-OUT =====")

    active_visitors = get_active_visitors()

    if not active_visitors:
        print("\nNo visitors are currently checked in.")
        return

    display_active_visitors(active_visitors)

    selected_visitor = select_active_visitor(active_visitors)

    if selected_visitor is None:
        print("\nCheck-out cancelled.")
        return

    complete_check_out(selected_visitor)


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
