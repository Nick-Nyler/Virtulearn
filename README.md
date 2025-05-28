# VIRTULEARN
Virtulearn is a CLI application for managing online courses, instructors, and student enrollments.

## Setup
1. Run `pipenv install` to install dependencies.
2. Run `python main.py` to start the CLI.

## Usage
Navigate menus to add, list, find, or delete instructors, courses, and enrollments:
- Select ‘1’ to manage instructors.
- Select ‘2’ to manage courses.
- Select ‘3’ to manage enrollments.
- Select ‘4’ to drop all tables (use with caution).
- Select ‘5’ to exit.

## Design Choices
- SQLite is used for simplicity, with `virtulearn.db` as the database file.
- `cascade='all, delete-orphan'` ensures data integrity by removing related records when an instructor or course is deleted.