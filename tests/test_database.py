import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.database import get_session
from lib.models.base import Base 

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


    def test_database_connection(self):
        try:
            session = self.Session() 
            self.assertIsNotNone(session)
            session.close()
        except Exception as e:
            self.fail(f"Database connection failed: {e}")

    def test_tables_created(self):
        session = self.Session()
        inspector = session.bind.dialect.inspector(session.bind)
        tables = inspector.get_table_names()

        self.assertIn('instructors', tables)
        self.assertIn('courses', tables)
        self.assertIn('enrollments', tables)
        session.close()

    def test_transaction_rollback(self):
        session = self.Session()
        from lib.models.instructor import Instructor 

        initial_count = session.query(Instructor).count()
        instructor = Instructor(name="Temp Instructor", email="temp@example.com")
        session.add(instructor)
        session.rollback() 
        new_count = session.query(Instructor).count()
        self.assertEqual(initial_count, new_count)
        session.close()
