from lib.database import Session
from lib.models.instructor import Instructor
from lib.models.course import Course

def get_instructor_summary():
    session = Session()
    instructors = session.query(Instructor).all()
    
    # Use a list to store instructor data as tuples
    instructor_list = []
    for instructor in instructors:
        course_count = len(instructor.courses)
        # Tuple for immutable instructor data
        instructor_data = (instructor.name, instructor.expertise, course_count)
        instructor_list.append(instructor_data)
    
    # Use a dictionary to count courses per instructor
    course_counts = {}
    for instructor in instructors:
        course_counts[instructor.name] = len(instructor.courses)
    
    session.close()
    return {"instructors": instructor_list, "course_counts": course_counts}