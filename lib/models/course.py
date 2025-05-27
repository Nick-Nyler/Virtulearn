from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from lib.database import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in hours
    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    instructor = relationship("Instructor", back_populates="courses")

Instructor.courses = relationship("Course", order_by=Course.id, back_populates="instructor")