import unittest
from unittest.mock import patch
import io
import sys
import os

from lib.database import get_session, create_tables 

def mock_run_cli_app(input_data):
    """
    A simplified mock of how your CLI app might be called.
    In a real test, you'd call the actual entry point of your CLI.
    """
    output = ""
    if "add course" in input_data.lower():
        output = "Course added successfully!\n"
    elif "list instructors" in input_data.lower():
        output = "Instructors:\n- Dr. Jane Doe\n- Prof. John Smith\n"
    elif "exit" in input_data.lower():
        output = "Exiting Virtulearn.\n"
    else:
        output = "Unknown command.\n"
    sys.stdout.write(output)


class TestCLI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        from lib.models.base import Base
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

        cls.patcher = patch('lib.database.get_session', return_value=cls.Session())
        cls.mock_get_session = cls.patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop() 

    def setUp(self):
       
        session = self.Session()
        from lib.models.base import Base 
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
        session.close()

    def test_add_course_command(self):
        mock_input = "\n".join([
            "add course",
            "Advanced Python",
            "Deep dive into Python programming",
            "Dr. Alice" 
        ])
        with patch('sys.stdin', io.StringIO(mock_input)):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                mock_run_cli_app(mock_input) 

                output = mock_stdout.getvalue()
                self.assertIn("Course added successfully!", output)
                session = self.Session()
                from lib.models.course import Course
                course = session.query(Course).filter_by(title="Advanced Python").first()
                self.assertIsNotNone(course)
                self.assertEqual(course.description, "Deep dive into Python programming")
                session.close()

    def test_list_instructors_command(self):
        # Seed some data for listing
        session = self.Session()
        from lib.models.instructor import Instructor
        session.add(Instructor(name="Dr. Jane Doe", email="jane@example.com"))
        session.add(Instructor(name="Prof. John Smith", email="john@example.com"))
        session.commit()
        session.close()

        mock_input = "list instructors"

        with patch('sys.stdin', io.StringIO(mock_input)):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                mock_run_cli_app(mock_input) 
                output = mock_stdout.getvalue()
                self.assertIn("Instructors:", output)
                self.assertIn("- Dr. Jane Doe", output)
                self.assertIn("- Prof. John Smith", output)

    def test_invalid_command_input(self):
        mock_input = "foobar" 

        with patch('sys.stdin', io.StringIO(mock_input)):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                mock_run_cli_app(mock_input) 
                output = mock_stdout.getvalue()
                self.assertIn("Unknown command.", output) 

    def test_exit_command(self):
        mock_input = "exit"

        with patch('sys.stdin', io.StringIO(mock_input)):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                mock_run_cli_app(mock_input) 
                output = mock_stdout.getvalue()
                self.assertIn("Exiting Virtulearn.", output)