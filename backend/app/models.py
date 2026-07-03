from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)   
    phone = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    photo_path = Column(String, nullable=True)