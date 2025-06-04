from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from lib.database import Base

class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    expertise = Column(String)
    email = Column(String, unique=True, index=True)

    courses = relationship("Course", back_populates="instructor")
    enrollments = relationship("Enrollment", back_populates="instructor")