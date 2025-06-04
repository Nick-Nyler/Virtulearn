from lib.database import create_db_tables
from lib.cli import perform_initdb, perform_dropdb, add_instructor_cli, list_instructors_cli, find_instructor_cli, delete_instructor_cli, add_course_cli, list_courses_cli, find_course_cli, delete_course_cli, assign_course_cli, add_enrollment_cli, list_enrollments_cli, find_enrollment_cli, delete_enrollment_cli, find_instructor_by_email_cli, find_enrollments_by_email_cli
import sys

def instructor_menu():
    while True:
        print("\n--- Manage Instructors ---")
        print("1. Add Instructor")
        print("2. List All Instructors")
        print("3. Find Instructor by ID")
        print("4. Find Instructor by Email")
        print("5. Delete Instructor")
        print("6. Back to Main Menu")
        choice = input("Select an option: ")
        options = {
            '1': add_instructor_cli,
            '2': list_instructors_cli,
            '3': find_instructor_cli,
            '4': find_instructor_by_email_cli,
            '5': delete_instructor_cli,
            '6': lambda: None
        }
        action = options.get(choice)
        if action:
            action()
        elif choice != '6':
            print("Invalid option. Please try again.")
        if choice == '6':
            break

def course_menu():
    while True:
        print("\n--- Manage Courses ---")
        print("1. Add Course")
        print("2. List All Courses")
        print("3. Find Course by ID")
        print("4. Delete Course")
        print("5. Assign Course to Instructor")
        print("6. Back to Main Menu")
        choice = input("Select an option: ")
        options = {
            '1': add_course_cli,
            '2': list_courses_cli,
            '3': find_course_cli,
            '4': delete_course_cli,
            '5': assign_course_cli,
            '6': lambda: None
        }
        action = options.get(choice)
        if action:
            action()
        elif choice != '6':
            print("Invalid option. Please try again.")
        if choice == '6':
            break

def enrollment_menu():
    while True:
        print("\n--- Manage Enrollments ---")
        print("1. Add Enrollment")
        print("2. List All Enrollments")
        print("3. Find Enrollment by ID")
        print("4. Find Enrollments by Email")
        print("5. Delete Enrollment")
        print("6. Back to Main Menu")
        choice = input("Select an option: ")
        options = {
            '1': add_enrollment_cli,
            '2': list_enrollments_cli,
            '3': find_enrollment_cli,
            '4': find_enrollments_by_email_cli,
            '5': delete_enrollment_cli,
            '6': lambda: None
        }
        action = options.get(choice)
        if action:
            action()
        elif choice != '6':
            print("Invalid option. Please try again.")
        if choice == '6':
            break

def main_menu():
    try:
        perform_initdb()
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        sys.exit(1)

    while True:
        print("\n--- Main Menu ---")
        print("1. Manage Instructors")
        print("2. Manage Courses")
        print("3. Manage Enrollments")
        print("4. Drop All Tables (DANGEROUS)")
        print("5. Exit")
        choice = input("Select an option: ")
        menu_options = {
            '1': instructor_menu,
            '2': course_menu,
            '3': enrollment_menu,
            '4': perform_dropdb,
            '5': lambda: (print("Exiting Virtulearn. Goodbye!"), sys.exit())
        }
        menu_options.get(choice, lambda: print("Invalid option. Please try again."))()

if __name__ == '__main__':
    main_menu()