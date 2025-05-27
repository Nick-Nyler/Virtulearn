from sqlalchemy import Column, Integer, String
from lib.database import Base

class Instructor(Base):
    __tablename__ = "instructors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    expertise = Column(String, nullable=False)