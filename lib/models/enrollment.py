from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from lib.database import Base
from datetime import datetime

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    student_name = Column(String, nullable=False)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    course = relationship("Course")