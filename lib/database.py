import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

Base = declarative_base()

from lib.models.instructor import Instructor
from lib.models.course import Course
from lib.models.enrollment import Enrollment

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///virtulearn.db")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def create_db_tables():
    try:
        Base.metadata.create_all(engine)
        print("Database tables created/checked.")
    except Exception as e:
        print(f"Error creating database tables: {e}")

def drop_db_tables():
    try:
        Base.metadata.drop_all(engine)
        print("Database tables dropped.")
    except Exception as e:
        print(f"Error dropping database tables: {e}")