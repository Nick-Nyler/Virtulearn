import unittest
from unittest.mock import patch, MagicMock
import io
import sys
import functools
import datetime

from lib.helpers import (
    validate_input,
    get_instructor_by_id,
    get_course_by_id,
    get_enrollment_by_id,
    log_query
)

from lib.models.instructor import Instructor
from lib.models.course import Course
from lib.models.enrollment import Enrollment

class TestHelpers(unittest.TestCase):

    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_validate_input_str_success(self):
        with patch('builtins.input', side_effect=["test string"]):
            result = validate_input("Enter text: ")
            self.assertEqual(result, "test string")
            self.assertEqual(self.held_output.getvalue(), "")

    def test_validate_input_str_empty_allowed(self):
        with patch('builtins.input', side_effect=[""]):
            result = validate_input("Enter text (optional): ")
            self.assertEqual(result, "")
            self.assertEqual(self.held_output.getvalue(), "")

    def test_validate_input_int_success(self):
        with patch('builtins.input', side_effect=["123"]):
            result = validate_input("Enter number: ", type_func=int)
            self.assertEqual(result, 123)
            self.assertEqual(self.held_output.getvalue(), "")

    def test_validate_input_int_invalid_then_valid(self):
        with patch('builtins.input', side_effect=["abc", "456"]):
            result = validate_input("Enter number: ", type_func=int)
            self.assertEqual(result, 456)
            output = self.held_output.getvalue()
            self.assertIn("Invalid input. Please enter a valid int.", output)
            self.assertNotIn("abc", output)

    def test_validate_input_int_empty_not_allowed(self):
        with patch('builtins.input', side_effect=["", "789"]):
            result = validate_input("Enter number: ", type_func=int)
            self.assertEqual(result, 789)
            output = self.held_output.getvalue()
            self.assertIn("Input cannot be empty. Please try again.", output)
            self.assertIn("Invalid input. Please enter a valid int.", output)

    def test_log_query_decorator_prints_messages(self):
        @log_query
        def dummy_function(session, arg1, kwarg1="default"):
            return "dummy result"

        mock_session = MagicMock()
        result = dummy_function(mock_session, "val1", kwarg1="val2")

        output = self.held_output.getvalue()
        self.assertIn("Queried dummy_function with args ('val1',), kwargs {'kwarg1': 'val2'}", output)
        self.assertIn("Result: dummy result", output)
        self.assertEqual(result, "dummy result")

    def test_log_query_decorator_preserves_attributes(self):
        @log_query
        def original_function(session, data):
            """Original function docstring."""
            return data

        self.assertEqual(original_function.__name__, "original_function")
        self.assertEqual(original_function.__doc__, "Original function docstring.")

    def test_get_instructor_by_id_found(self):
        mock_instructor = Instructor(id=1, name="Test Instructor", expertise="Testing")
        mock_session = MagicMock()
        mock_session.query(Instructor).get.return_value = mock_instructor

        result = get_instructor_by_id(mock_session, 1)

        mock_session.query(Instructor).get.assert_called_once_with(1)
        self.assertEqual(result, mock_instructor)
        output = self.held_output.getvalue()
        self.assertIn("Queried get_instructor_by_id with args (1,), kwargs {}", output)
        self.assertIn(f"Result: {mock_instructor}", output)

    def test_get_instructor_by_id_not_found(self):
        mock_session = MagicMock()
        mock_session.query(Instructor).get.return_value = None

        result = get_instructor_by_id(mock_session, 999)

        mock_session.query(Instructor).get.assert_called_once_with(999)
        self.assertIsNone(result)
        output = self.held_output.getvalue()
        self.assertIn("Queried get_instructor_by_id with args (999,), kwargs {}", output)
        self.assertIn("Result: None", output)

    def test_get_course_by_id_found(self):
        mock_course = Course(id=1, title="Test Course", duration=30)
        mock_session = MagicMock()
        mock_session.query(Course).get.return_value = mock_course

        result = get_course_by_id(mock_session, 1)

        mock_session.query(Course).get.assert_called_once_with(1)
        self.assertEqual(result, mock_course)
        output = self.held_output.getvalue()
        self.assertIn("Queried get_course_by_id with args (1,), kwargs {}", output)
        self.assertIn(f"Result: {mock_course}", output)

    def test_get_course_by_id_not_found(self):
        mock_session = MagicMock()
        mock_session.query(Course).get.return_value = None

        result = get_course_by_id(mock_session, 999)

        mock_session.query(Course).get.assert_called_once_with(999)
        self.assertIsNone(result)
        output = self.held_output.getvalue()
        self.assertIn("Queried get_course_by_id with args (999,), kwargs {}", output)
        self.assertIn("Result: None", output)

    def test_get_enrollment_by_id_found(self):
        mock_enrollment = Enrollment(id=1, student_name="Test Student", enrollment_date=datetime.datetime.now())
        mock_session = MagicMock()
        mock_session.query(Enrollment).get.return_value = mock_enrollment

        result = get_enrollment_by_id(mock_session, 1)

        mock_session.query(Enrollment).get.assert_called_once_with(1)
        self.assertEqual(result, mock_enrollment)
        output = self.held_output.getvalue()
        self.assertIn("Queried get_enrollment_by_id with args (1,), kwargs {}", output)
        self.assertIn(f"Result: {mock_enrollment}", output)

    def test_get_enrollment_by_id_not_found(self):
        mock_session = MagicMock()
        mock_session.query(Enrollment).get.return_value = None

        result = get_enrollment_by_id(mock_session, 999)

        mock_session.query(Enrollment).get.assert_called_once_with(999)
        self.assertIsNone(result)
        output = self.held_output.getvalue()
        self.assertIn("Queried get_enrollment_by_id with args (999,), kwargs {}", output)
        self.assertIn("Result: None", output)