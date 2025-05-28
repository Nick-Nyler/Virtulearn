from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from lib.database import Base

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    duration = Column(Integer)
    instructor_id = Column(Integer, ForeignKey('instructors.id'))

    instructor = relationship('Instructor', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', duration='{self.duration}', instructor={self.instructor.name if self.instructor else self.instructor_id})>"