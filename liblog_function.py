from datetime import datetime
import os
from csv_handler import CSVStorage
from visitor_record import VisitorRecord

MAX_CAPACITY = 20


class LibraryLogSystem:
    """Main controller class for visitor check-in, check-out, and occupancy."""

    def __init__(self, storage=None, max_capacity=MAX_CAPACITY):
        self._storage = storage or CSVStorage()
        self._max_capacity = max_capacity
        self._visitors = [
            VisitorRecord.from_dict(row)
            for row in self._storage.load_data()
        ]

    def get_today(self):
        return datetime.now().strftime("%Y-%m-%d")

    def is_today(self, visitor):
        return visitor.is_for_date(self.get_today())

    def get_current_occupancy(self):
        return len(self.get_active_visitors())

    def get_active_visitors(self):
        today = self.get_today()
        return [
            visitor
            for visitor in self._visitors
            if visitor.is_active_on(today)
        ]

    def has_active_visitor(self, name):
        return any(
            visitor.matches_name(name)
            for visitor in self.get_active_visitors()
        )

    def check_in_visitor(self, name, reason, address, school, signature):
        visitor = VisitorRecord.create(
            name=name,
            reason=reason,
            address=address,
            school=school,
            signature=signature,
        )

        self._visitors.append(visitor)
        self._storage.append_record(visitor.to_dict())

        return visitor

    def check_out_visitor(self, visitor):
        duration = visitor.check_out()
        self._storage.save_all(self.to_dict_list())

        return duration

    def get_visitors(self):
        return list(self._visitors)

    def get_max_capacity(self):
        return self._max_capacity

    def to_dict_list(self):
        return [visitor.to_dict() for visitor in self._visitors]


system = LibraryLogSystem()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def get_today():
    return system.get_today()


def is_today(visitor):
    return system.is_today(visitor)


def get_current_occupancy():
    return system.get_current_occupancy()


def get_active_visitors():
    return system.get_active_visitors()


def has_active_visitor(name):
    return system.has_active_visitor(name)


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

    if get_current_occupancy() >= get_max_capacity():
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

    visitor = system.check_in_visitor(
        name=name,
        reason=reason,
        address=address,
        school=school,
        signature=signature,
    )

    print("\nCheck-in successful!")
    print("Date:", visitor.date)
    print("Time In:", visitor.time_in)
    print("Current Occupancy:", get_current_occupancy())


# =========================
# FEATURE 2: CHECK OUT
# =========================
def display_active_visitors(active_visitors):
    print("\nVisitors Currently Inside:")
    print("--------------------------")

    for index, visitor in enumerate(active_visitors, start=1):
        print(f"{index}. {visitor.name}")

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
    duration = system.check_out_visitor(visitor)

    print("\nCheck-out successful!")
    print("Name:", visitor.name)
    print("Time Out:", visitor.time_out)
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
    max_capacity = get_max_capacity()
    percent = (inside / max_capacity) * 100

    print("===== OCCUPANCY =====")
    print("Current Occupancy:", inside)
    print("Maximum Capacity:", max_capacity)
    print(f"Percentage Full: {percent:.2f}%")

    if inside >= max_capacity:
        print("WARNING: Library is FULL!")
    elif inside >= max_capacity * 0.8:
        print("WARNING: Library is NEAR CAPACITY!")
    else:
        print("Library occupancy is normal.")


# =========================
# HELPER FUNCTIONS
# =========================
def get_visitors():
    return system.get_visitors()


def get_max_capacity():
    return system.get_max_capacity()
