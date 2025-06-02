import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models.base import Base 
from lib.models.instructor import Instructor
from lib.models.course import Course
from lib.models.enrollment import Enrollment

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()

    def test_instructor_creation(self):
        instructor = Instructor(name="Dr. Smith", email="smith@example.com")
        self.session.add(instructor)
        self.session.commit()
        retrieved_instructor = self.session.query(Instructor).filter_by(name="Dr. Smith").first()
        self.assertIsNotNone(retrieved_instructor)
        self.assertEqual(retrieved_instructor.email, "smith@example.com")

    def test_instructor_update(self):
        instructor = Instructor(name="Old Name", email="old@example.com")
        self.session.add(instructor)
        self.session.commit()
        instructor.name = "New Name"
        self.session.commit()
        updated_instructor = self.session.query(Instructor).filter_by(email="old@example.com").first()
        self.assertEqual(updated_instructor.name, "New Name")

    def test_instructor_deletion(self):
        instructor = Instructor(name="Instructor to Delete", email="delete@example.com")
        self.session.add(instructor)
        self.session.commit()
        self.session.delete(instructor)
        self.session.commit()
        deleted_instructor = self.session.query(Instructor).filter_by(name="Instructor to Delete").first()
        self.assertIsNone(deleted_instructor)

    def test_course_creation(self):
        instructor = Instructor(name="Dr. Jones", email="jones@example.com")
        self.session.add(instructor)
        self.session.commit()

        course = Course(title="Calculus I", description="Intro to Calculus", instructor=instructor)
        self.session.add(course)
        self.session.commit()

        retrieved_course = self.session.query(Course).filter_by(title="Calculus I").first()
        self.assertIsNotNone(retrieved_course)
        self.assertEqual(retrieved_course.instructor.name, "Dr. Jones")

    def test_course_relationship_with_instructor(self):
        instructor = Instructor(name="Prof. Green", email="green@example.com")
        course1 = Course(title="Physics I", description="Mechanics")
        course2 = Course(title="Physics II", description="Electromagnetism")

        instructor.courses.append(course1)
        instructor.courses.append(course2)
        self.session.add(instructor)
        self.session.commit()

        retrieved_instructor = self.session.query(Instructor).filter_by(name="Prof. Green").first()
        self.assertEqual(len(retrieved_instructor.courses), 2)
        self.assertIn("Physics I", [c.title for c in retrieved_instructor.courses])

    def test_enrollment_creation(self):
        instructor = Instructor(name="Dr. Lee", email="lee@example.com")
        course = Course(title="Data Structures", description="Advanced Data Structures")
        self.session.add_all([instructor, course])
        self.session.commit()

        enrollment = Enrollment(student_name="Alice", course=course)
        self.session.add(enrollment)
        self.session.commit()

        retrieved_enrollment = self.session.query(Enrollment).filter_by(student_name="Alice").first()
        self.assertIsNotNone(retrieved_enrollment)
        self.assertEqual(retrieved_enrollment.course.title, "Data Structures")

    def test_course_relationship_with_enrollments(self):
        instructor = Instructor(name="Dr. Kim", email="kim@example.com")
        course = Course(title="Algorithms", description="Advanced Algorithms", instructor=instructor)
        enrollment1 = Enrollment(student_name="Bob")
        enrollment2 = Enrollment(student_name="Carol")

        course.enrollments.append(enrollment1)
        course.enrollments.append(enrollment2)
        self.session.add_all([instructor, course])
        self.session.commit()

        retrieved_course = self.session.query(Course).filter_by(title="Algorithms").first()
        self.assertEqual(len(retrieved_course.enrollments), 2)
        self.assertIn("Bob", [e.student_name for e in retrieved_course.enrollments])