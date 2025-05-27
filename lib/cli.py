import click
from lib.database import Session
from lib.models.instructor import Instructor
from lib.models.course import Course
from lib.models.enrollment import Enrollment
from lib.helpers import get_instructor_summary

@click.group()
def cli():
    """VirtuLearn CLI: Manage instructors and courses for an e-learning platform"""
    pass

@cli.command()
@click.argument("name")
@click.argument("expertise")
def add_instructor(name, expertise):
    """Add a new instructor"""
    session = Session()
    try:
        instructor = Instructor(name=name, expertise=expertise)
        session.add(instructor)
        session.commit()
        click.echo(f"Added instructor: {name} (Expertise: {expertise})")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

@cli.command()
def list_instructors():
    """List all instructors"""
    session = Session()
    instructors = session.query(Instructor).all()
    if not instructors:
        click.echo("No instructors found.")
        return
    for instructor in instructors:
        click.echo(f"ID: {instructor.id}, Name: {instructor.name}, Expertise: {instructor.expertise}")
    session.close()

@cli.command()
@click.argument("instructor_id", type=int)
def find_instructor(instructor_id):
    """Find an instructor by ID"""
    session = Session()
    instructor = session.query(Instructor).get(instructor_id)
    if instructor:
        click.echo(f"ID: {instructor.id}, Name: {instructor.name}, Expertise: {instructor.expertise}")
    else:
        click.echo(f"Instructor with ID {instructor_id} not found.")
    session.close()

@cli.command()
@click.argument("title")
@click.argument("duration", type=int)
@click.argument("instructor_id", type=int)
def add_course(title, duration, instructor_id):
    """Add a new course"""
    session = Session()
    try:
        instructor = session.query(Instructor).get(instructor_id)
        if not instructor:
            click.echo(f"Instructor with ID {instructor_id} not found.")
            return
        course = Course(title=title, duration=duration, instructor_id=instructor_id)
        session.add(course)
        session.commit()
        click.echo(f"Added course: {title} (Duration: {duration} hours)")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

@cli.command()
def list_courses():
    """List all courses"""
    session = Session()
    courses = session.query(Course).all()
    if not courses:
        click.echo("No courses found.")
        return
    for course in courses:
        instructor = session.query(Instructor).get(course.instructor_id)
        click.echo(f"ID: {course.id}, Title: {course.title}, Duration: {course.duration} hours, Instructor: {instructor.name}")
    session.close()

@cli.command()
@click.argument("course_id", type=int)
def find_course(course_id):
    """Find a course by ID"""
    session = Session()
    course = session.query(Course).get(course_id)
    if course:
        instructor = session.query(Instructor).get(course.instructor_id)
        click.echo(f"ID: {course.id}, Title: {course.title}, Duration: {course.duration} hours, Instructor: {instructor.name}")
    else:
        click.echo(f"Course with ID {course_id} not found.")
    session.close()

@cli.command()
@click.argument("instructor_id", type=int)
def instructor_courses(instructor_id):
    """List all courses for an instructor"""
    session = Session()
    instructor = session.query(Instructor).get(instructor_id)
    if not instructor:
        click.echo(f"Instructor with ID {instructor_id} not found.")
        return
    courses = instructor.courses
    if not courses:
        click.echo(f"No courses found for {instructor.name}.")
        return
    click.echo(f"Courses taught by {instructor.name}:")
    for course in courses:
        click.echo(f"ID: {course.id}, Title: {course.title}, Duration: {course.duration} hours")
    session.close()

@cli.command()
@click.argument("course_id", type=int)
@click.argument("student_name")
def add_enrollment(course_id, student_name):
    """Enroll a student in a course"""
    session = Session()
    try:
        course = session.query(Course).get(course_id)
        if not course:
            click.echo(f"Course with ID {course_id} not found.")
            return
        enrollment = Enrollment(course_id=course_id, student_name=student_name)
        session.add(enrollment)
        session.commit()
        click.echo(f"Enrolled {student_name} in {course.title}")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

@cli.command()
def summary():
    """Show a summary of instructors and their courses"""
    summary = get_instructor_summary()
    click.echo("Instructor Summary:")
    for instructor_data in summary["instructors"]:
        click.echo(f"Instructor: {instructor_data[0]}, Expertise: {instructor_data[1]}, Courses: {instructor_data[2]}")
    click.echo("\nCourse Count per Instructor:")
    for name, count in summary["course_counts"].items():
        click.echo(f"{name}: {count} courses")

if __name__ == "__main__":
    cli()