from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from lib.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    enrollment_date = Column(DateTime)
    student_email = Column(String, index=True) 

    course = relationship("Course", back_populates="enrollments")
    instructor = relationship("Instructor", back_populates="enrollments")