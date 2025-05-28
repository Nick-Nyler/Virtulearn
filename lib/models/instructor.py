from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.database import Base

class Instructor(Base):
    __tablename__ = 'instructors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    expertise = Column(String, nullable=False)

    courses = relationship('Course', back_populates='instructor', cascade='all, delete-orphan')
    enrollments = relationship('Enrollment', back_populates='instructor', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Instructor(id={self.id}, name='{self.name}', expertise='{self.expertise}', courses={len(self.courses)})>"