from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import employees
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates

from app.routers import employees, pages 


app = FastAPI(
    title="Реестр сотрудников",
    description="Тестовое задание: CRUD с фильтрацией и пагинацией",
    version="1.0.0"
)

# Настройка CORS (разрешаем все источники для удобства разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
app.include_router(employees.router)
app.include_router(pages.router) 


# Корневой эндпоинт для проверки
@app.get("/")
def root():
    return {"message": "API Реестра сотрудников работает. Документация: /docs"}