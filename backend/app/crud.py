from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from datetime import date
from dateutil.relativedelta import relativedelta
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate



def get_employees(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    gender: Optional[str] = None,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
) -> List[Employee]:
    
    query = db.query(Employee)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Employee.surname.ilike(search_term),
                Employee.first_name.ilike(search_term),
                Employee.patronymic.ilike(search_term),
                Employee.phone.ilike(search_term)
            )
        )

    if gender:
        query = query.filter(Employee.gender == gender)

    today = date.today()
    if age_max is not None:
        min_birth_date = today - relativedelta(years=age_max)
        query = query.filter(Employee.birth_date >= min_birth_date)
    if age_min is not None:
        max_birth_date = today - relativedelta(years=age_min)
        query = query.filter(Employee.birth_date <= max_birth_date)

    return query.offset(skip).limit(limit).all()

def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.id == employee_id).first()

def create_employee(db: Session, employee: EmployeeCreate, photo_path: Optional[str] = None) -> Employee:
    db_employee = Employee(**employee.model_dump(), photo_path=photo_path)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee_update: EmployeeUpdate, photo_path: Optional[str] = None) -> Optional[Employee]:
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None
    update_data = employee_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
    if photo_path is not None:
        db_employee.photo_path = photo_path
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int) -> bool:
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return False
    db.delete(db_employee)
    db.commit()
    return True

def count_employees(
    db: Session,
    search: Optional[str] = None,
    gender: Optional[str] = None,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None) -> int:
    query = db.query(Employee)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Employee.surname.ilike(search_term),
                Employee.first_name.ilike(search_term),
                Employee.patronymic.ilike(search_term),
                Employee.phone.ilike(search_term)
            )
        )
    if gender:
        query = query.filter(Employee.gender == gender)

    today = date.today()
    if age_max is not None:
        min_birth_date = today - relativedelta(years=age_max)
        query = query.filter(Employee.birth_date >= min_birth_date)
    if age_min is not None:
        max_birth_date = today - relativedelta(years=age_min)
        query = query.filter(Employee.birth_date <= max_birth_date)

    return query.count()