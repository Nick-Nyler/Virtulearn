# Online Course Platform

A Python CLI application for managing instructors and courses on an e-learning platform, built with SQLAlchemy ORM and Click.

## Installation
1. Clone the repository: `git clone <repo-url>`
2. Navigate to the project directory: `cd online_course_platform`
3. Install dependencies: `pipenv install`
4. Activate the virtual environment: `pipenv shell`
5. Run the application: `python main.py --help`

## Usage
- Add an instructor: `python main.py add-instructor "Jane Doe" "Python Programming"`
- List instructors: `python main.py list-instructors`
- Find instructor by ID: `python main.py find-instructor 1`
- Add a course: `python main.py add-course "Intro to Python" 10 1`
- List courses: `python main.py list-courses`
- Find course by ID: `python main.py find-course 1`
- List courses by instructor: `python main.py instructor-courses 1`
- Enroll a student: `python main.py add-enrollment 1 "Alice Johnson"`
- View summary: `python main.py summary`
- List courses using raw SQL: `python main.py sql-instructor-courses 1`

## Database
- The application uses a SQLite database (`courses.db`), created automatically when running `python main.py`.
- Tables: `instructors`, `courses`, `enrollments`.
- SQLAlchemy ORM manages database operations, with optional raw SQL in `lib/sql_operations.py`.

## Learning Goals
- **CLI**: Built with Click for a user-friendly interface.
- **ORM**: Uses SQLAlchemy with three related tables and one-to-many relationships.
- **Data Structures**: Lists, dictionaries, and tuples in `helpers.py` for summarizing data.
- **Virtual Environment**: Managed with Pipenv.
- **Best Practices**: Modular code, error handling, input validation, PEP 8 compliance.
- **SQL (Optional)**: Raw SQL queries in `sql_operations.py` for table creation and data retrieval.

## Project Structure
- `courses.db`: SQLite database (generated after running the app).
- `lib/models/`: SQLAlchemy models for database tables.
- `lib/cli.py`: CLI commands using Click.
- `lib/database.py`: Database setup and connection.
- `lib/helpers.py`: Utility functions for data processing.
- `lib/sql_operations.py`: Optional raw SQL operations.
- `main.py`: Application entry point.