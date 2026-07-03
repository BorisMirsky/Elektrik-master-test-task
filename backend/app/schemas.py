from pydantic import BaseModel, Field, field_validator, computed_field
from datetime import date
from typing import Optional

class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Имя сотрудника")
    birth_date: date = Field(..., description="Дата рождения")
    phone: str = Field(..., min_length=1, description="Номер телефона")
    gender: str = Field(..., pattern="^(male|female)$", description="Пол (male/female)")

    @field_validator("name", "phone")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip()

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    birth_date: Optional[date] = None
    phone: Optional[str] = Field(None, min_length=1)
    gender: Optional[str] = Field(None, pattern="^(male|female)$")

    @field_validator("name", "phone")
    def not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip() if v is not None else v

class EmployeeOut(BaseModel):
    id: int
    name: str
    birth_date: date
    phone: str
    gender: str
    photo_path: Optional[str] = None

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        # Вычисляем возраст (учитываем день рождения)
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    class Config:
        from_attributes = True  # позволяет работать с SQLAlchemy-моделями