from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, computed_field, field_validator
import re


class EmployeeCreate(BaseModel):
    surname: str = Field(..., min_length=1)
    first_name: str = Field(..., min_length=1)
    patronymic: Optional[str] = Field(None, min_length=0)
    birth_date: date
    phone: Optional[str] = None
    gender: str = Field(..., pattern="^(male|female)$")

    @field_validator("surname", "first_name")
    def validate_name(cls, v):
        if not re.match(r"^[A-Za-zА-Яа-яЁё\s\-]+$", v):
            raise ValueError("Допустимы только буквы, пробелы и дефис")
        return v.strip()

    # @field_validator("patronymic")
    # def validate_patronymic(cls, v):
    #     if v is not None and v != "" and not re.match(r"^[A-Za-zА-Яа-яЁё\s\-]+$", v):
    #         raise ValueError("Допустимы только буквы, пробелы и дефис")
    #     return v.strip() if v else None

    @field_validator("patronymic")
    def validate_patronymic(cls, v):
        if v is None or v == "":
            return None
        if not re.match(r"^[A-Za-zА-Яа-яЁё\s\-]+$", v):
            raise ValueError("Допустимы только буквы, пробелы и дефис")
        return v.strip()

    @field_validator("phone")
    def validate_phone(cls, v):
        if v is None or v == "":
            return None
        digits = re.sub(r"\D", "", v)
        if len(digits) != 11:
            raise ValueError("Номер должен содержать 11 цифр")
        return f"+{digits}"


class EmployeeUpdate(BaseModel):
    surname: Optional[str] = Field(None, min_length=1)
    first_name: Optional[str] = Field(None, min_length=1)
    patronymic: Optional[str] = Field(None, min_length=0)
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    gender: Optional[str] = Field(None, pattern="^(male|female)$")


    @field_validator("surname", "first_name")
    def validate_name(cls, v):
        if v is not None and not re.match(r"^[A-Za-zА-Яа-яЁё\s\-]+$", v):
            raise ValueError("Допустимы только буквы, пробелы и дефис")
        return v.strip() if v else v

    # @field_validator("patronymic")
    # def validate_patronymic(cls, v):
    #     if v is not None and v != "" and not re.match(r"^[A-Za-zА-Яа-яЁё\s\-]+$", v):
    #         raise ValueError("Допустимы только буквы, пробелы и дефис")
    #     return v.strip() if v else None
    

    @field_validator("patronymic")
    def validate_patronymic(cls, v):
        if v is None or v == "":
            return None
        if not re.match(r"^[A-Za-zА-Яа-яЁё\s\-]+$", v):
            raise ValueError("Допустимы только буквы, пробелы и дефис")
        return v.strip()

    @field_validator("phone")
    def validate_phone(cls, v):
        if v is None or v == "":
            return None
        digits = re.sub(r"\D", "", v)
        if len(digits) != 11:
            raise ValueError("Номер должен содержать 11 цифр")
        return f"+{digits}"

class EmployeeOut(BaseModel):
    id: int
    surname: str
    first_name: str
    patronymic: Optional[str] = None
    birth_date: date
    phone: Optional[str] = None
    gender: str
    photo_path: Optional[str] = None

    @computed_field
    @property
    def full_name(self) -> str:
        parts = [self.surname, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return " ".join(parts)

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    class Config:
        from_attributes = True