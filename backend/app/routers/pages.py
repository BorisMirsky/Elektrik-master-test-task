from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.crud import get_employees, get_employee, create_employee, update_employee, delete_employee, count_employees
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut 
from app.file_utils import save_upload_file
from fastapi.templating import Jinja2Templates
import os
from datetime import datetime



templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))

router = APIRouter(prefix="", tags=["pages"])


@router.get("/")
def index(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100),
    search: Optional[str] = None,
    gender: Optional[str] = None,
    age_min: Optional[str] = None,
    age_max: Optional[str] = None,
):
    # Преобразуем пустые строки в None
    if gender == "":
        gender = None
    if gender not in [None, "male", "female"]:
        gender = None  # игнорируем некорректные значения

    # Преобразуем age_min и age_max в int, если они не пустые
    age_min_int = None
    age_max_int = None
    if age_min is not None and age_min.isdigit():
        age_min_int = int(age_min)
    if age_max is not None and age_max.isdigit():
        age_max_int = int(age_max)

    # Пагинация
    skip = (page - 1) * limit

    # Получаем сотрудников с фильтрацией
    employees = get_employees(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        gender=gender,
        age_min=age_min_int,
        age_max=age_max_int
    )
    
    employees_out = [EmployeeOut.model_validate(emp) for emp in employees]

    # Общее количество (для пагинации)
    total_employees = count_employees(
        db=db,
        search=search,
        gender=gender,
        age_min=age_min_int,
        age_max=age_max_int
    )
    total_pages = (total_employees + limit - 1) // limit  # округление вверх

    # Флаги для кнопок "Назад"/"Вперёд" (опционально, если используешь)
    has_next = page < total_pages
    has_prev = page > 1

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "employees": employees_out,
            "page": page,
            "limit": limit,
            "search": search or "",
            "gender": gender or "",
            "age_min": age_min or "",
            "age_max": age_max or "",
            "total_pages": total_pages,
            "total_employees": total_employees,
            "has_next": has_next,
            "has_prev": has_prev,
        }
    )


@router.get("/employees/create")
def create_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "employee": None})


@router.post("/employees/create")
async def create_employee_handler(
    db: Session = Depends(get_db),
    surname: str = Form(...),
    first_name: str = Form(...),
    patronymic: str = Form(""),
    phone: str = Form(""),
    birth_date: Optional[str] = Form(None),
    gender: str = Form(...),
    photo: Optional[UploadFile] = File(None),
):
    patronymic_val = patronymic if patronymic != "" else None
    phone_val = phone if phone != "" else None

    # Преобразуем строку в дату
    try:
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты (нужно YYYY-MM-DD)")

    employee_data = EmployeeCreate(
        surname=surname,
        first_name=first_name,
        patronymic=patronymic_val,
        birth_date=birth_date_obj,
        phone=phone_val,
        gender=gender
    )
    photo_path = None
    if photo and photo.filename:
        photo_path = await save_upload_file(photo)
    create_employee(db, employee_data, photo_path)
    return RedirectResponse(url="/", status_code=303)


@router.get("/employees/{employee_id}/edit")
def edit_form(request: Request, employee_id: int, db: Session = Depends(get_db)):
    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return templates.TemplateResponse(
        "form.html",
        {"request": request, "employee": employee}
    )


@router.post("/employees/{employee_id}/edit")
async def update_employee_handler(
    employee_id: int,
    db: Session = Depends(get_db),
    surname: str = Form(...),
    first_name: str = Form(...),
    patronymic: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
):

    patronymic_val = patronymic if patronymic != "" else None
    phone_val = phone if phone != "" else None
    update_data = {
        "surname": surname,
        "first_name": first_name,
        "patronymic": patronymic_val,  
        "phone": phone_val,             
        "gender": gender,
    }
    employee_update = EmployeeUpdate(**update_data)   
    photo_path = None
    if photo and photo.filename:
        photo_path = await save_upload_file(photo)
    updated = update_employee(db, employee_id, employee_update, photo_path)
    if not updated:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return RedirectResponse(url="/", status_code=303)



@router.post("/employees/{employee_id}/delete")
def delete_employee_handler(
    employee_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")    
    return RedirectResponse(url="/", status_code=303)