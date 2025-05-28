from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from lib.database import Base

class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True)
    student_name = Column(String, nullable=False)
    enrollment_date = Column(DateTime, nullable=False)
    instructor_id = Column(Integer, ForeignKey('instructors.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

    instructor = relationship('Instructor', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')

    def __repr__(self):
        return f"<Enrollment(id={self.id}, student='{self.student_name}', course={self.course.title if self.course else self.course_id}, instructor={self.instructor.name if self.instructor else self.instructor_id})>"