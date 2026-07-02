from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import employees

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

# Подключаем роутер
app.include_router(employees.router)

# Корневой эндпоинт для проверки
@app.get("/")
def root():
    return {"message": "API Реестра сотрудников работает. Документация: /docs"}