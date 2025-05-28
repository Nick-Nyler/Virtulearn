import functools
from sqlalchemy.orm import Session
from lib.models.instructor import Instructor
from lib.models.course import Course
from lib.models.enrollment import Enrollment

def log_query(func):
    @functools.wraps(func)
    def wrapper(session: Session, *args, **kwargs):
        print(f"Queried {func.__name__} with args {args}, kwargs {kwargs}")
        result = func(session, *args, **kwargs)
        print(f"Result: {result}")
        return result
    return wrapper

def validate_input(prompt: str, type_func=str):
    """
    Prompts the user for input and validates its type.
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input and type_func != str:
            print("Input cannot be empty. Please try again.")
            continue
        try:
            return type_func(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {type_func.__name__}.")

@log_query
def get_instructor_by_id(session: Session, instructor_id: int) -> Instructor | None:
    """
    Retrieves an Instructor object by its ID.
    Returns Instructor ORM object or None if not found.
    """
    return session.query(Instructor).get(instructor_id)

@log_query
def get_course_by_id(session: Session, course_id: int) -> Course | None:
    """
    Retrieves a Course object by its ID.
    Returns Course ORM object or None if not found.
    """
    return session.query(Course).get(course_id)

@log_query
def get_enrollment_by_id(session: Session, enrollment_id: int) -> Enrollment | None:
    """
    Retrieves an Enrollment object by its ID.
    Returns Enrollment ORM object or None if not found.
    """
    return session.query(Enrollment).get(enrollment_id)