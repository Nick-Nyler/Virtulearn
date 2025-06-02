import unittest
from unittest.mock import patch, MagicMock
import io
import sys

from main import main_menu, instructor_menu, course_menu, enrollment_menu

class TestMainMenu(unittest.TestCase):

    def setUp(self):
        self.patcher_initdb = patch('lib.cli.perform_initdb')
        self.patcher_dropdb = patch('lib.cli.perform_dropdb')
        self.patcher_add_instructor = patch('lib.cli.add_instructor_cli')
        self.patcher_list_instructors = patch('lib.cli.list_instructors_cli')
        self.patcher_find_instructor = patch('lib.cli.find_instructor_cli')
        self.patcher_delete_instructor = patch('lib.cli.delete_instructor_cli')
        self.patcher_add_course = patch('lib.cli.add_course_cli')
        self.patcher_list_courses = patch('lib.cli.list_courses_cli')
        self.patcher_find_course = patch('lib.cli.find_course_cli')
        self.patcher_delete_course = patch('lib.cli.delete_course_cli')
        self.patcher_assign_course = patch('lib.cli.assign_course_cli')
        self.patcher_add_enrollment = patch('lib.cli.add_enrollment_cli')
        self.patcher_list_enrollments = patch('lib.cli.list_enrollments_cli')
        self.patcher_find_enrollment = patch('lib.cli.find_enrollment_cli')
        self.patcher_delete_enrollment = patch('lib.cli.delete_enrollment_cli')

        self.mock_initdb = self.patcher_initdb.start()
        self.mock_dropdb = self.patcher_dropdb.start()
        self.mock_add_instructor = self.patcher_add_instructor.start()
        self.mock_list_instructors = self.patcher_list_instructors.start()
        self.mock_find_instructor = self.patcher_find_instructor.start()
        self.mock_delete_instructor = self.patcher_delete_instructor.start()
        self.mock_add_course = self.patcher_add_course.start()
        self.mock_list_courses = self.patcher_list_courses.start()
        self.mock_find_course = self.patcher_find_course.start()
        self.mock_delete_course = self.patcher_delete_course.start()
        self.mock_assign_course = self.patcher_assign_course.start()
        self.mock_add_enrollment = self.patcher_add_enrollment.start()
        self.mock_list_enrollments = self.patcher_list_enrollments.start()
        self.mock_find_enrollment = self.patcher_find_enrollment.start()
        self.mock_delete_enrollment = self.patcher_delete_enrollment.start()

        self.patcher_sys_exit = patch('sys.exit')
        self.mock_sys_exit = self.patcher_sys_exit.start()

        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        self.patcher_initdb.stop()
        self.patcher_dropdb.stop()
        self.patcher_add_instructor.stop()
        self.patcher_list_instructors.stop()
        self.patcher_find_instructor.stop()
        self.patcher_delete_instructor.stop()
        self.patcher_add_course.stop()
        self.patcher_list_courses.stop()
        self.patcher_find_course.stop()
        self.patcher_delete_course.stop()
        self.patcher_assign_course.stop()
        self.patcher_add_enrollment.stop()
        self.patcher_list_enrollments.stop()
        self.patcher_find_enrollment.stop()
        self.patcher_delete_enrollment.stop()
        self.patcher_sys_exit.stop()

        sys.stdout = sys.__stdout__

        for mock in [
            self.mock_initdb, self.mock_dropdb, self.mock_add_instructor,
            self.mock_list_instructors, self.mock_find_instructor, self.mock_delete_instructor,
            self.mock_add_course, self.mock_list_courses, self.mock_find_course,
            self.mock_delete_course, self.mock_assign_course, self.mock_add_enrollment,
            self.mock_list_enrollments, self.mock_find_enrollment, self.mock_delete_enrollment,
            self.mock_sys_exit
        ]:
            mock.reset_mock()

    def simulate_menu_input(self, inputs):
        return patch('builtins.input', side_effect=inputs)

    def test_main_menu_initializes_db(self):
        with self.simulate_menu_input(["5"]):
            main_menu()
            self.mock_initdb.assert_called_once()
            self.mock_sys_exit.assert_called_once()

    def test_main_menu_handles_initdb_failure(self):
        self.mock_initdb.side_effect = Exception("DB Init Failed")
        with self.simulate_menu_input(["5"]):
            main_menu()
            self.mock_initdb.assert_called_once()
            self.mock_sys_exit.assert_called_once_with(1)
            self.assertIn("Failed to initialize database: DB Init Failed", self.held_output.getvalue())

    def test_main_menu_exit_option(self):
        with self.simulate_menu_input(["5"]):
            main_menu()
            self.mock_sys_exit.assert_called_once()
            self.assertIn("Exiting Virtulearn. Goodbye!", self.held_output.getvalue())

    def test_main_menu_invalid_option(self):
        with self.simulate_menu_input(["99", "5"]):
            main_menu()
            self.assertIn("Invalid option. Please try again.", self.held_output.getvalue())
            self.mock_sys_exit.assert_called_once()

    def test_main_menu_drop_tables_option(self):
        with self.simulate_menu_input(["4", "5"]):
            main_menu()
            self.mock_dropdb.assert_called_once()
            self.mock_sys_exit.assert_called_once()

    def test_main_menu_to_instructor_menu_and_back(self):
        with self.simulate_menu_input(["1", "5", "5"]):
            main_menu()
            self.mock_add_instructor.assert_not_called()
            self.mock_sys_exit.assert_called_once()
            output = self.held_output.getvalue()
            self.assertIn("--- Manage Instructors ---", output)

    def test_instructor_menu_add_instructor(self):
        with self.simulate_menu_input(["1", "1", "5", "5"]):
            main_menu()
            self.mock_add_instructor.assert_called_once()
            self.mock_sys_exit.assert_called_once()

    def test_instructor_menu_list_instructors(self):
        with self.simulate_menu_input(["1", "2", "5", "5"]):
            main_menu()
            self.mock_list_instructors.assert_called_once()

    def test_instructor_menu_find_instructor(self):
        with self.simulate_menu_input(["1", "3", "5", "5"]):
            main_menu()
            self.mock_find_instructor.assert_called_once()

    def test_instructor_menu_delete_instructor(self):
        with self.simulate_menu_input(["1", "4", "5", "5"]):
            main_menu()
            self.mock_delete_instructor.assert_called_once()

    def test_instructor_menu_invalid_option(self):
        with self.simulate_menu_input(["1", "99", "5", "5"]):
            main_menu()
            self.assertIn("Invalid option. Please try again.", self.held_output.getvalue())
            self.mock_sys_exit.assert_called_once()

    def test_main_menu_to_course_menu_and_back(self):
        with self.simulate_menu_input(["2", "6", "5"]):
            main_menu()
            self.mock_add_course.assert_not_called()
            self.mock_sys_exit.assert_called_once()
            output = self.held_output.getvalue()
            self.assertIn("--- Manage Courses ---", output)

    def test_course_menu_add_course(self):
        with self.simulate_menu_input(["2", "1", "6", "5"]):
            main_menu()
            self.mock_add_course.assert_called_once()

    def test_course_menu_list_courses(self):
        with self.simulate_menu_input(["2", "2", "6", "5"]):
            main_menu()
            self.mock_list_courses.assert_called_once()

    def test_course_menu_find_course(self):
        with self.simulate_menu_input(["2", "3", "6", "5"]):
            main_menu()
            self.mock_find_course.assert_called_once()

    def test_course_menu_delete_course(self):
        with self.simulate_menu_input(["2", "4", "6", "5"]):
            main_menu()
            self.mock_delete_course.assert_called_once()

    def test_course_menu_assign_course(self):
        with self.simulate_menu_input(["2", "5", "6", "5"]):
            main_menu()
            self.mock_assign_course.assert_called_once()

    def test_course_menu_invalid_option(self):
        with self.simulate_menu_input(["2", "99", "6", "5"]):
            main_menu()
            self.assertIn("Invalid option. Please try again.", self.held_output.getvalue())
            self.mock_sys_exit.assert_called_once()

    def test_main_menu_to_enrollment_menu_and_back(self):
        with self.simulate_menu_input(["3", "5", "5"]):
            main_menu()
            self.mock_add_enrollment.assert_not_called()
            self.mock_sys_exit.assert_called_once()
            output = self.held_output.getvalue()
            self.assertIn("--- Manage Enrollments ---", output)

    def test_enrollment_menu_add_enrollment(self):
        with self.simulate_menu_input(["3", "1", "5", "5"]):
            main_menu()
            self.mock_add_enrollment.assert_called_once()

    def test_enrollment_menu_list_enrollments(self):
        with self.simulate_menu_input(["3", "2", "5", "5"]):
            main_menu()
            self.mock_list_enrollments.assert_called_once()

    def test_enrollment_menu_find_enrollment(self):
        with self.simulate_menu_input(["3", "3", "5", "5"]):
            main_menu()
            self.mock_find_enrollment.assert_called_once()

    def test_enrollment_menu_delete_enrollment(self):
        with self.simulate_menu_input(["3", "4", "5", "5"]):
            main_menu()
            self.mock_delete_enrollment.assert_called_once()

    def test_enrollment_menu_invalid_option(self):
        with self.simulate_menu_input(["3", "99", "5", "5"]):
            main_menu()
            self.assertIn("Invalid option. Please try again.", self.held_output.getvalue())
            self.mock_sys_exit.assert_called_once()