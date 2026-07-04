from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut
from app.crud import (
    get_employees, get_employee, create_employee,
    update_employee, delete_employee
)

router = APIRouter(prefix="/api/employees", tags=["employees"])

@router.get("/", response_model=List[EmployeeOut])
def read_employees(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    gender: Optional[str] = Query(None, pattern="^(male|female)$"),
    age_min: Optional[int] = Query(None, ge=0),
    age_max: Optional[int] = Query(None, ge=0)
):

    employees = get_employees(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        gender=gender,
        age_min=age_min,
        age_max=age_max
    )
    return employees


@router.get("/{employee_id}", response_model=EmployeeOut)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return employee


@router.post("/", response_model=EmployeeOut, status_code=201)
def create_employee_endpoint(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db, employee)


@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee_endpoint(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    updated = update_employee(db, employee_id, employee_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return updated


@router.delete("/{employee_id}", status_code=204)
def delete_employee_endpoint(employee_id: int, db: Session = Depends(get_db)):
    """Удалить сотрудника."""
    deleted = delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return  # 204 No Content