from pydantic import BaseModel, Field, field_validator
from typing import Optional

class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Имя сотрудника")
    age: int = Field(..., gt=0, description="Возраст (положительное число)")
    phone: str = Field(..., min_length=1, description="Номер телефона")
    gender: str = Field(..., pattern="^(male|female)$", description="Пол: male или female")

    @field_validator("name", "phone")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip()

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    age: Optional[int] = Field(None, gt=0)
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
    age: int
    phone: str
    gender: str
    photo_path: Optional[str] = None

    class Config:
        from_attributes = True  # для совместимости с SQLAlchemy (ранее orm_mode)