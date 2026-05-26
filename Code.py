from datetime import datetime
import os

# =========================
# FUNCTION: CLEAR SCREEN
# =========================
def clear_screen():

    # For Windows
    if os.name == "nt":
        os.system("cls")

    # For Mac/Linux
    else:
        os.system("clear")


# =========================
# LIBLOG CONSOLE SYSTEM
# =========================

# List to store visitor records
visitors = []

# Library settings
MAX_CAPACITY = 20
current_occupancy = 0


# =========================
# FUNCTION: CHECK IN
# =========================
def check_in():
    global current_occupancy

    clear_screen()

    # Check if library is full
    if current_occupancy >= MAX_CAPACITY:
        print("\nLibrary is already at full capacity!")
        return

    print("\n===== VISITOR CHECK-IN =====")

    # User inputs
    name = input("Enter full name: ")
    reason = input("Enter reason of visit: ")
    address = input("Enter address: ")
    school = input("Enter school name: ")

    # Automatic date and time
    time_in = datetime.now()

    # Create visitor record
    visitor = {
        "name": name,
        "reason": reason,
        "address": address,
        "school": school,
        "time_in": time_in,
        "time_out": None,
        "duration": None
    }

    # Save to list
    visitors.append(visitor)

    # Increase occupancy
    current_occupancy += 1

    print("\nVisitor checked in successfully!")
    print("Time In:", time_in.strftime("%Y-%m-%d %H:%M:%S"))


# =========================
# FUNCTION: CHECK OUT
# =========================
def check_out():
    global current_occupancy

    clear_screen()

    print("\n===== VISITOR CHECK-OUT =====")

    name = input("Enter visitor name: ")

    found = False

    # Search for visitor
    for visitor in visitors:

        # Check if visitor is still inside
        if visitor["name"].lower() == name.lower() and visitor["time_out"] is None:

            time_out = datetime.now()

            # Save time out
            visitor["time_out"] = time_out

            # Calculate duration
            duration = time_out - visitor["time_in"]
            visitor["duration"] = duration

            # Decrease occupancy
            current_occupancy -= 1

            print("\nVisitor checked out successfully!")
            print("Time Out:", time_out.strftime("%Y-%m-%d %H:%M:%S"))
            print("Visit Duration:", duration)

            found = True
            break

    if not found:
        print("\nVisitor record not found or already checked out.")


# =========================
# FUNCTION: VIEW OCCUPANCY
# =========================
def view_occupancy():

    clear_screen()

    print("\n===== LIVE OCCUPANCY =====")

    percentage = (current_occupancy / MAX_CAPACITY) * 100

    print("Current Occupancy:", current_occupancy)
    print("Maximum Capacity:", MAX_CAPACITY)
    print("Percentage Full: {:.2f}%".format(percentage))

    # Warnings
    if current_occupancy == MAX_CAPACITY:
        print("WARNING: Library is FULL!")

    elif current_occupancy >= MAX_CAPACITY * 0.8:
        print("WARNING: Library is NEAR CAPACITY!")

    else:
        print("Library occupancy is normal.")


# =========================
# FUNCTION: GENERATE REPORT
# =========================
def generate_report():

    clear_screen()

    print("\n===== DAILY REPORT =====")

    total_checkins = len(visitors)

    visitors_inside = 0
    completed_visits = 0
    total_duration_seconds = 0

    # Analyze records
    for visitor in visitors:

        if visitor["time_out"] is None:
            visitors_inside += 1

        else:
            completed_visits += 1
            total_duration_seconds += visitor["duration"].total_seconds()

    # Calculate average duration
    if completed_visits > 0:
        average_seconds = total_duration_seconds / completed_visits
        average_minutes = average_seconds / 60
    else:
        average_minutes = 0

    # Display report
    print("Total Check-Ins:", total_checkins)
    print("Visitors Still Inside:", visitors_inside)
    print("Completed Visits:", completed_visits)
    print("Average Visit Duration: {:.2f} minutes".format(average_minutes))


# =========================
# MAIN MENU
# =========================
def main():

    while True:

        clear_screen()

        print("\n==============================")
        print("       LIBLOG CONSOLE")
        print("==============================")
        print("1. Check In Visitor")
        print("2. Check Out Visitor")
        print("3. View Occupancy")
        print("4. Generate Report")
        print("5. Exit")
        print("==============================")

        choice = input("Enter your choice: ")

        # MENU OPTIONS
        if choice == "1":
            check_in()

        elif choice == "2":
            check_out()

        elif choice == "3":
            view_occupancy()

        elif choice == "4":
            generate_report()

        elif choice == "5":
            clear_screen()
            print("\nExiting LibLog Console...")
            print("Thank you for using the system!")
            break

        else:
            print("\nInvalid choice! Please try again.")

        # Pause before returning to menu
        input("\nPress Enter to return to the menu...")


# =========================
# START PROGRAM
# =========================
main()