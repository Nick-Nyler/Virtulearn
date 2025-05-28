# VirtuLearn: A Command-Line Learning Management System

## Table of Contents
1. [About VirtuLearn](#1-about-virtulearn)
2. [Features](#2-features)
3. [Technologies Used](#3-technologies-used)
4. [Database Schema](#4-database-schema)
5. [Setup and Installation](#5-setup-and-installation)
6. [Usage](#6-usage)
7. [Future Enhancements](#7-future-enhancements)
8. [License](#8-license)
9. [Author](#9-author)

## 1. About VirtuLearn

VirtuLearn is a simple, console-based Learning Management System (LMS) designed to help manage instructors, courses, and student enrollments. Built with Python and SQLAlchemy, it provides a command-line interface (CLI) for interacting with a SQLite database, demonstrating fundamental concepts of Object-Relational Mapping (ORM) and database management in a Python application.

## 2. Features

### Instructor Management:
- Add new instructors with name and expertise.
- List all instructors with their assigned courses and student enrollments.
- Find instructor details by ID.
- Delete instructors (along with their associated courses and enrollments, if configured).

### Course Management:
- Add new courses with title, duration, and an optional assigned instructor.
- List all courses with their assigned instructor and enrolled students.
- Find course details by ID.
- Delete courses.
- Assign an existing course to an existing instructor.

### Enrollment Management:
- Enroll students in courses, optionally linking to a specific instructor and specifying an enrollment date.
- List all enrollments with student name, course title, instructor, and date.
- Find enrollment details by ID.
- Delete enrollments.

### Database Management:
- Initializes database tables on startup if they don't exist.
- Option to drop all tables (for development/testing).

## 3. Technologies Used

- **[Python](https://www.python.org/)** – The core programming language.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** – Python SQL Toolkit and Object Relational Mapper.
- **[SQLite3](https://www.sqlite.org/)** – Lightweight, file-based SQL database.
- **[Pipenv](https://pipenv.pypa.io/en/latest/)** – Dependency management and virtual environment tool.

## 4. Database Schema

VirtuLearn uses three main entities: `Instructor`, `Course`, and `Enrollment`.

```
+--------------+      +--------------+      +----------------+
| Instructors  |      |   Courses    |      |   Enrollments  |
+--------------+      +--------------+      +----------------+
| id (PK)      |<-----| instructor_id|      | id (PK)        |
| name         |      | id (PK)      |<-----| course_id      |
| expertise    |      | title        |      | student_name   |
+--------------+      | duration     |      | enrollment_date|
                      +--------------+      | instructor_id  |
                                            +----------------+
```

- **Instructors:** One-to-many with Courses and Enrollments.
- **Courses:** One-to-many with Enrollments.
- **Enrollments:** Link students to Courses and optionally to Instructors.

## 5. Setup and Installation

### Prerequisites

- Python 3.12
- Pipenv (install via `pip install pipenv`)

### Installation Steps

1. **Clone the Repository:**

```bash
git clone https://github.com/Nick-Nyler/Virtulearn.git
cd Virtulearn
```

2. **Install Dependencies using Pipenv:**

```bash
pipenv install
```

3. **Activate the Virtual Environment:**

```bash
pipenv shell
```

Your terminal prompt should indicate you're in the `virtulearn` virtual environment.

## 6. Usage

Once the virtual environment is activated, run the application:

```bash
python main.py
```

You will be presented with the main menu:

```
--- Main Menu ---
1. Manage Instructors
2. Manage Courses
3. Manage Enrollments
4. Drop All Tables (DANGEROUS)
5. Exit
```

Follow the on-screen prompts to navigate and perform operations.

**Important Notes:**
- The database (`virtulearn.db`) is created on first run.
- If you modify model definitions in `lib/models/*.py`, delete `virtulearn.db` and rerun `python main.py` to reflect changes.

## 7. Future Enhancements

- **Student Model:** Add a dedicated Student model with fields like name and email.
- **User Authentication:** Support roles like admin, instructor, and student.
- **Robust CLI:** Use Click or other libraries for improved CLI UX.
- **Reporting:** Generate reports like courses by instructor or students per course.
- **Validation:** Add better input validation.
- **Web Interface:** Build a web UI using Flask or Django.

## 8. Author

**Your Name** – [GitHub](https://github.com/Nick-Nyler) | [LinkedIn](https://www.linkedin.com/in/nixon-ochieng-a9a623218)