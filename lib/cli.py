from sqlalchemy.exc import IntegrityError
from lib.database import get_session, create_db_tables, drop_db_tables
from lib.models.instructor import Instructor
from lib.models.course import Course
from lib.models.enrollment import Enrollment
from lib.helpers import validate_input, get_instructor_by_id, get_course_by_id, get_enrollment_by_id
from datetime import datetime

def perform_initdb():
    create_db_tables()
    print("Database tables created/checked successfully.")

def perform_dropdb():
    confirm = input("Are you sure you want to drop all database tables? (yes/no): ").lower()
    if confirm == 'yes':
        drop_db_tables()
        print("Database tables dropped.")
    else:
        print("Operation cancelled.")

def add_instructor_cli():
    with get_session() as session:
        name = validate_input("Enter instructor name: ")
        expertise = validate_input("Enter instructor expertise: ")
        try:
            instructor = Instructor(name=name, expertise=expertise)
            session.add(instructor)
            session.commit()
            print(f"Instructor '{name}' added successfully with ID: {instructor.id}")
        except IntegrityError:
            session.rollback()
            print(f"Error: An instructor with the name '{name}' already exists.")
        except Exception as e:
            session.rollback()
            print(f"An unexpected error occurred: {e}")

def list_instructors_cli():
    with get_session() as session:
        instructors = session.query(Instructor).all()
        if instructors:
            print("\n--- All Instructors ---")
            for instr in instructors:
                print(f"ID: {instr.id}, Name: {instr.name}, Expertise: {instr.expertise}")
                if instr.courses:
                    print("  Courses Taught:")
                    for course in instr.courses:
                        print(f"    - {course.title} ({course.duration})")
                else:
                    print("  No courses assigned.")
                if instr.enrollments:
                    print("  Student Enrollments:")
                    for enroll in instr.enrollments:
                        course_title = enroll.course.title if enroll.course else 'N/A (Course Deleted)'
                        print(f"    - Student: {enroll.student_name}, Course: {course_title}")
                print("-" * 20)
            print("-----------------------")
        else:
            print("No instructors found.")

def find_instructor_cli():
    with get_session() as session:
        instructor_id = validate_input("Enter instructor ID: ", type_func=int)
        instructor = get_instructor_by_id(session, instructor_id)
        if instructor:
            print(f"\n--- Instructor Details (ID: {instructor_id}) ---")
            print(f"Name: {instructor.name}") 
            print(f"Expertise: {instructor.expertise}") 
            if instructor.courses:
                print("Courses Taught:")
                for course in instructor.courses:
                    print(f"  - {course.title} ({course.duration})")
            else:
                print("No courses assigned.")
            if instructor.enrollments:
                print("Student Enrollments:")
                for enroll in instructor.enrollments:
                    print(f"  - Student: {enroll.student_name}, Course: {enroll.course.title if enroll.course else 'N/A'}")
        else:
            print(f"Instructor with ID {instructor_id} not found.")

def delete_instructor_cli():
    with get_session() as session:
        instructor_id = validate_input("Enter instructor ID to delete: ", type_func=int)
        instructor = get_instructor_by_id(session, instructor_id)
        if instructor:
            confirm = input(f"Are you sure you want to delete instructor '{instructor.name}' and all their associated data? (yes/no): ").lower() # Access directly
            if confirm == 'yes':
                try:
                    session.delete(instructor)
                    session.commit()
                    print(f"Instructor '{instructor.name}' and associated data deleted successfully.") # Access directly
                except Exception as e:
                    session.rollback()
                    print(f"An error occurred while deleting instructor: {e}")
            else:
                print("Deletion cancelled.")
        else:
            print(f"Instructor with ID {instructor_id} not found.")

def add_course_cli():
    with get_session() as session:
        title = validate_input("Enter course title: ")
        duration = validate_input("Enter course duration (e.g., 30): ", type_func=int)
        instructor_id_str = input("Enter instructor ID for this course (optional, leave blank if none): ").strip()
        instructor_id = int(instructor_id_str) if instructor_id_str else None

        try:
            instructor = None
            if instructor_id:
                instructor = get_instructor_by_id(session, instructor_id)
                if not instructor:
                    print(f"Error: Instructor with ID {instructor_id} not found. Course will be added without an instructor.")
                    instructor_id = None

            course = Course(title=title, duration=duration, instructor_id=instructor_id)
            session.add(course)
            session.commit()
            if instructor:
                print(f"Course '{title}' added successfully with ID: {course.id} and assigned to '{instructor.name}'.") # Access directly
            else:
                print(f"Course '{title}' added successfully with ID: {course.id}")
        except IntegrityError:
            session.rollback()
            print(f"Error: A course with the title '{title}' already exists.")
        except Exception as e:
            session.rollback()
            print(f"An unexpected error occurred: {e}")

def list_courses_cli():
    with get_session() as session:
        courses = session.query(Course).all()
        if courses:
            print("\n--- All Courses ---")
            for crs in courses:
                instructor_name = crs.instructor.name if crs.instructor else "N/A (No Instructor)"
                print(f"ID: {crs.id}, Title: {crs.title}, Duration: {crs.duration}, Instructor: {instructor_name}")
                if crs.enrollments:
                    print("  Enrolled Students:")
                    for enroll in crs.enrollments:
                        enrollment_date_str = enroll.enrollment_date.strftime('%Y-%m-%d') if enroll.enrollment_date else 'N/A'
                        print(f"    - {enroll.student_name} (Enrolled: {enrollment_date_str})")
                print("-" * 20)
            print("-------------------")
        else:
            print("No courses found.")

def find_course_cli():
    with get_session() as session:
        course_id = validate_input("Enter course ID: ", type_func=int)
        course = get_course_by_id(session, course_id)
        if course:
            instructor_name = course.instructor.name if course.instructor else "N/A (No Instructor)"
            print(f"\n--- Course Details (ID: {course_id}) ---")
            print(f"Title: {course.title}")
            print(f"Duration: {course.duration}")
            print(f"Instructor: {instructor_name}")
            if course.enrollments:
                print("Enrolled Students:")
                for enroll in course.enrollments:
                    enrollment_date_str = enroll.enrollment_date.strftime('%Y-%m-%d') if enroll.enrollment_date else 'N/A'
                    print(f"  - {enroll.student_name} (Enrolled: {enrollment_date_str})")
        else:
            print(f"Course with ID {course_id} not found.")

def delete_course_cli():
    with get_session() as session:
        course_id = validate_input("Enter course ID to delete: ", type_func=int)
        course = get_course_by_id(session, course_id) 
        if course:
            confirm = input(f"Are you sure you want to delete course '{course.title}'? (yes/no): ").lower()
            if confirm == 'yes':
                try:
                    session.delete(course)
                    session.commit()
                    print(f"Course '{course.title}' deleted successfully.")
                except Exception as e:
                    session.rollback()
                    print(f"An error occurred while deleting course: {e}")
            else:
                print("Deletion cancelled.")
        else:
            print(f"Course with ID {course_id} not found.")

def assign_course_cli():
    with get_session() as session:
        course_id = validate_input("Enter course ID to assign: ", type_func=int)
        instructor_id = validate_input("Enter instructor ID to assign to: ", type_func=int)
        course = get_course_by_id(session, course_id)
        instructor = get_instructor_by_id(session, instructor_id)

        if not course:
            print(f"Error: Course with ID {course_id} not found.")
            return
        if not instructor:
            print(f"Error: Instructor with ID {instructor_id} not found.")
            return

        try:
            course.instructor = instructor
            session.commit() 
            print(f"Course '{course.title}' successfully assigned to instructor '{instructor.name}'.") # Access directly
        except Exception as e:
            session.rollback()
            print(f"An error occurred while assigning course: {e}")

def add_enrollment_cli():
    with get_session() as session:
        student_name = validate_input("Enter student name: ")
        course_id = validate_input("Enter course ID for enrollment: ", type_func=int)

        instructor_id_str = input("Enter instructor ID for this enrollment (optional, leave blank if not specific): ").strip()
        instructor_id = int(instructor_id_str) if instructor_id_str else None

        enrollment_date_str = input("Enter enrollment date (YYYY-MM-DD, default today if blank): ").strip()

        enrollment_date_obj = None
        if not enrollment_date_str:
            enrollment_date_obj = datetime.now()
        else:
            try:
                enrollment_date_obj = datetime.strptime(enrollment_date_str, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Using today's date.")
                enrollment_date_obj = datetime.now()

        try:
            course = get_course_by_id(session, course_id)
            if not course:
                print(f"Error: Course with ID {course_id} not found.")
                return

            final_instructor_id_for_enrollment = None
            if instructor_id:
                instructor_obj = get_instructor_by_id(session, instructor_id)
                if not instructor_obj:
                    print(f"Warning: Instructor with ID {instructor_id} not found. Enrollment will proceed without linking to a specific instructor from user input.")
                else:
                    final_instructor_id_for_enrollment = instructor_obj.id
            elif course.instructor_id:
                final_instructor_id_for_enrollment = course.instructor_id

            enrollment = Enrollment(
                student_name=student_name,
                course_id=course_id,
                instructor_id=final_instructor_id_for_enrollment,
                enrollment_date=enrollment_date_obj 
            )
            session.add(enrollment)
            session.commit()
            print(f"Student '{student_name}' enrolled in course '{course.title}' (Enrollment ID: {enrollment.id}).")
        except Exception as e:
            session.rollback()
            print(f"An unexpected error occurred during enrollment: {e}")

def list_enrollments_cli():
    with get_session() as session:
        enrollments = session.query(Enrollment).all()
        if enrollments:
            print("\n--- All Enrollments ---")
            for enroll in enrollments:
                course_title = enroll.course.title if enroll.course else "N/A (Course Deleted)"
                instructor_name = enroll.instructor.name if enroll.instructor else "N/A (No Instructor)"
                enrollment_date_str = enroll.enrollment_date.strftime('%Y-%m-%d') if enroll.enrollment_date else 'N/A'
                print(f"ID: {enroll.id}, Student: {enroll.student_name}, Course: {course_title}, Instructor: {instructor_name}, Date: {enrollment_date_str}")
            print("-----------------------")
        else:
            print("No enrollments found.")

def find_enrollment_cli():
    with get_session() as session:
        enrollment_id = validate_input("Enter enrollment ID: ", type_func=int)
        enrollment = get_enrollment_by_id(session, enrollment_id)
        if enrollment:
            course_title = enrollment.course.title if enrollment.course else "N/A (Course Deleted)"
            instructor_name = enrollment.instructor.name if enrollment.instructor else "N/A (No Instructor)"
            enrollment_date_str = enrollment.enrollment_date.strftime('%Y-%m-%d') if enrollment.enrollment_date else 'N/A'
            print(f"\n--- Enrollment Details (ID: {enrollment_id}) ---")
            print(f"Student: {enrollment.student_name}")
            print(f"Course: {course_title}")
            print(f"Instructor: {instructor_name}")
            print(f"Enrollment Date: {enrollment_date_str}")
        else:
            print(f"Enrollment with ID {enrollment_id} not found.")

def delete_enrollment_cli():
    with get_session() as session:
        enrollment_id = validate_input("Enter enrollment ID to delete: ", type_func=int)
        enrollment = get_enrollment_by_id(session, enrollment_id)
        if enrollment:
            confirm = input(f"Are you sure you want to delete enrollment ID {enrollment.id} for student '{enrollment.student_name}' in course '{enrollment.course.title if enrollment.course else 'N/A'}'? (yes/no): ").lower()
            if confirm == 'yes':
                try:
                    session.delete(enrollment)
                    session.commit()
                    print(f"Enrollment ID {enrollment.id} deleted successfully.")
                except Exception as e:
                    session.rollback()
                    print(f"An error occurred while deleting enrollment: {e}")
            else:
                print("Deletion cancelled.")
        else:
            print(f"Enrollment with ID {enrollment_id} not found.")