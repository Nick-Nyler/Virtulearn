from lib.database import Session
from lib.models.instructor import Instructor

def get_instructor_summary():
    session = Session()
    instructors = session.query(Instructor).all()

    instructor_list = []
    for instructor in instructors:
        course_count = len(instructor.courses)
        instructor_data = (instructor.name, instructor.expertise, course_count)
        instructor_list.append(instructor_data)
    
    course_counts = {}
    for instructor in instructors:
        course_counts[instructor.name] = len(instructor.courses)
    
    session.close()
    return {"instructors": instructor_list, "course_counts": course_counts}