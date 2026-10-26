import sys

try:
    from add_student import add_student
    from get_student import get_student
    from update_student import update_student
    from delete_student import delete_student
    from list_students import list_students
    from search_students import search_students
    from query_demo import query_demo
    from create_table import create_table
    from delete_table import delete_table
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all the .py files are in the same folder as main.py.")
    sys.exit(1)


def menu():
    while True:
        print("\n=========================================")
        print("          STUDENT MANAGER")
        print("=========================================")
        print("  1. Add Student          6. Search Students")
        print("  2. Get Student          7. Query demo")
        print("  3. Update Student       8. Create Table")
        print("  4. Delete Student       9. DELETE Table")
        print("  5. List Students        0. Exit")
        print("=========================================")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            get_student()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            list_students()
        elif choice == "6":
            search_students()
        elif choice == "7":
            query_demo()
        elif choice == "8":
            create_table()
        elif choice == "9":
            delete_table()
        elif choice == "0":
            print("Exiting Student Manager. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    menu()
