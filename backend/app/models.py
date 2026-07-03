from sqlalchemy import Column, Integer, String, Date
from app.database import Base



class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)  # отчество необязательно
    birth_date = Column(Date, nullable=False)
    phone = Column(String, nullable=True)  # теперь необязательно
    gender = Column(String, nullable=False)
    photo_path = Column(String, nullable=True)