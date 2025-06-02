import unittest
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from lib.database import Base

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
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def create_instructor(self, name="Test Instructor", expertise="Default Expertise"):
        instructor = Instructor(name=name, expertise=expertise)
        self.session.add(instructor)
        self.session.commit()
        return instructor

    def create_course(self, title="Test Course", duration=40, instructor=None):
        if instructor is None:
            instructor = self.create_instructor()
        course = Course(title=title, duration=duration, instructor=instructor)
        self.session.add(course)
        self.session.commit()
        return course

    def create_enrollment(self, student_name="Test Student", course=None, instructor=None):
        if course is None:
            course = self.create_course()
        if instructor is None:
            instructor = course.instructor
        enrollment_date = datetime.datetime.now()
        enrollment = Enrollment(
            student_name=student_name,
            enrollment_date=enrollment_date,
            instructor=instructor,
            course=course
        )
        self.session.add(enrollment)
        self.session.commit()
        return enrollment

    def test_instructor_creation_with_valid_data(self):
        instructor = self.create_instructor(name="Dr. Smith", expertise="Physics")
        retrieved_instructor = self.session.query(Instructor).filter_by(name="Dr. Smith").first()
        self.assertIsNotNone(retrieved_instructor)
        self.assertEqual(retrieved_instructor.name, "Dr. Smith")
        self.assertEqual(retrieved_instructor.expertise, "Physics")

    def test_instructor_name_uniqueness(self):
        self.create_instructor(name="Dr. Jane Doe", expertise="Chemistry")
        new_instructor = Instructor(name="Dr. Jane Doe", expertise="Biology")
        self.session.add(new_instructor)
        with self.assertRaises(IntegrityError):
            self.session.commit()
        self.session.rollback()

    def test_instructor_nullable_constraints(self):
        instructor_missing_name = Instructor(expertise="Math")
        self.session.add(instructor_missing_name)
        with self.assertRaises(IntegrityError):
            self.session.commit()
        self.session.rollback()

        instructor_missing_expertise = Instructor(name="Prof. Empty")
        self.session.add(instructor_missing_expertise)
        with self.assertRaises(IntegrityError):
            self.session.commit()
        self.session.rollback()

    def test_instructor_relationship_to_courses(self):
        instructor = self.create_instructor(name="Prof. Plum", expertise="Mystery")
        course1 = self.create_course(title="Clue Solving 101", instructor=instructor)
        course2 = self.create_course(title="Forensic Science", instructor=instructor)

        retrieved_instructor = self.session.query(Instructor).filter_by(name="Prof. Plum").first()
        self.assertEqual(len(retrieved_instructor.courses), 2)
        self.assertIn(course1, retrieved_instructor.courses)
        self.assertIn(course2, retrieved_instructor.courses)

    def test_instructor_relationship_to_enrollments(self):
        instructor = self.create_instructor(name="Colonel Mustard", expertise="Tactics")
        course = self.create_course(title="Strategic Planning", instructor=instructor)
        enrollment1 = self.create_enrollment(student_name="Private Green", course=course, instructor=instructor)
        enrollment2 = self.create_enrollment(student_name="Sergeant White", course=course, instructor=instructor)

        retrieved_instructor = self.session.query(Instructor).filter_by(name="Colonel Mustard").first()
        self.assertEqual(len(retrieved_instructor.enrollments), 2)
        self.assertIn(enrollment1, retrieved_instructor.enrollments)
        self.assertIn(enrollment2, retrieved_instructor.enrollments)

    def test_instructor_repr(self):
        instructor = self.create_instructor(id=1, name="Ms. Scarlet", expertise="Deduction")
        self.create_course(title="Investigative Techniques", instructor=instructor)
        retrieved_instructor = self.session.query(Instructor).filter_by(id=1).first()

        expected_repr = f"<Instructor(id=1, name='Ms. Scarlet', expertise='Deduction', courses=1)>"
        self.assertEqual(str(retrieved_instructor), expected_repr)

    def test_cascade_delete_courses_and_enrollments_from_instructor(self):
        instructor = self.create_instructor(name="Chef White", expertise="Cooking")
        course1 = self.create_course(title="Baking Basics", instructor=instructor)
        course2 = self.create_course(title="Advanced Pastries", instructor=instructor)
        enrollment1 = self.create_enrollment(student_name="Cook 1", course=course1, instructor=instructor)
        enrollment2 = self.create_enrollment(student_name="Cook 2", course=course2, instructor=instructor)

        self.assertEqual(self.session.query(Instructor).count(), 1)
        self.assertEqual(self.session.query(Course).count(), 2)
        self.assertEqual(self.session.query(Enrollment).count(), 2)

        self.session.delete(instructor)
        self.session.commit()

        self.assertEqual(self.session.query(Instructor).count(), 0)
        self.assertEqual(self.session.query(Course).count(), 0)
        self.assertEqual(self.session.query(Enrollment).count(), 0)

    def test_course_creation_with_valid_data(self):
        instructor = self.create_instructor()
        course = Course(title="Introduction to SQL", duration=40, instructor=instructor)
        self.session.add(course)
        self.session.commit()

        retrieved_course = self.session.query(Course).filter_by(title="Introduction to SQL").first()
        self.assertIsNotNone(retrieved_course)
        self.assertEqual(retrieved_course.title, "Introduction to SQL")
        self.assertEqual(retrieved_course.duration, 40)
        self.assertEqual(retrieved_course.instructor_id, instructor.id)
        self.assertEqual(retrieved_course.instructor.name, "Test Instructor")

    def test_course_title_uniqueness(self):
        instructor = self.create_instructor()
        self.create_course(title="Data Science Basics", duration=60, instructor=instructor)

        course2 = Course(title="Data Science Basics", duration=30, instructor=instructor)
        self.session.add(course2)
        with self.assertRaises(IntegrityError):
            self.session.commit()
        self.session.rollback()

    def test_cascade_delete_enrollments_from_course(self):
        instructor = self.create_instructor(name="Rogue Instructor")
        course = self.create_course(title="Absorption 101", instructor=instructor)
        enrollment_date = datetime.datetime.now()

        enrollment1 = Enrollment(student_name="Student X", enrollment_date=enrollment_date, instructor=instructor, course=course)
        enrollment2 = Enrollment(student_name="Student Y", enrollment_date=enrollment_date, instructor=instructor, course=course)
        self.session.add_all([enrollment1, enrollment2])
        self.session.commit()

        self.assertEqual(self.session.query(Enrollment).count(), 2)

        self.session.delete(course)
        self.session.commit()

        self.assertEqual(self.session.query(Enrollment).count(), 0)
        self.assertEqual(self.session.query(Course).count(), 0)

    def test_enrollment_creation_with_valid_data(self):
        instructor = self.create_instructor(name="Prof. X")
        course = self.create_course(title="Mutant History", instructor=instructor)
        enrollment_date = datetime.datetime.now()

        enrollment = Enrollment(
            student_name="Jean Grey",
            enrollment_date=enrollment_date,
            instructor=instructor,
            course=course
        )
        self.session.add(enrollment)
        self.session.commit()

        retrieved_enrollment = self.session.query(Enrollment).filter_by(student_name="Jean Grey").first()
        self.assertIsNotNone(retrieved_enrollment)
        self.assertEqual(retrieved_enrollment.student_name, "Jean Grey")
        self.assertEqual(retrieved_enrollment.instructor.name, "Prof. X")
        self.assertEqual(retrieved_enrollment.course.title, "Mutant History")

    def test_enrollment_nullable_constraints(self):
        instructor = self.create_instructor()
        course = self.create_course(instructor=instructor)

        enrollment_missing_name = Enrollment(
            enrollment_date=datetime.datetime.now(),
            instructor=instructor,
            course=course
        )
        self.session.add(enrollment_missing_name)
        with self.assertRaises(IntegrityError):
            self.session.commit()
        self.session.rollback()

        enrollment_missing_date = Enrollment(
            student_name="Cyclops",
            instructor=instructor,
            course=course
        )
        self.session.add(enrollment_missing_date)
        with self.assertRaises(IntegrityError):
            self.session.commit()
        self.session.rollback()

    def test_enrollment_repr(self):
        instructor = self.create_instructor(name="Beast")
        course = self.create_course(title="Genetics 101", instructor=instructor)
        enrollment = self.create_enrollment(student_name="Nightcrawler", course=course, instructor=instructor)

        expected_repr = f"<Enrollment(id={enrollment.id}, student='Nightcrawler', course=Genetics 101, instructor=Beast)>"
        self.assertEqual(str(enrollment), expected_repr)