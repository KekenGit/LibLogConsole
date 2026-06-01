from liblog_function import check_in, check_out, view_occupancy
from report_generator import generate_report
from liblog_function import clear_screen


def main():

    while True:

        clear_screen()

        print("======================")
        print("   LIBLOG CONSOLE")
        print("======================")
        print("1. Check In Visitor")
        print("2. Check Out Visitor")
        print("3. View Occupancy")
        print("4. Generate Report")
        print("5. Exit")
        print("======================")

        choice = input("Enter choice: ")

        if choice == "1":
            check_in()

        elif choice == "2":
            check_out()

        elif choice == "3":
            view_occupancy()

        elif choice == "4":
            generate_report()

        elif choice == "5":
            print("Exiting system...")
            break

        else:
            print("Invalid choice!")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
