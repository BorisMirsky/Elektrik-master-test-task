
# Elektrik-master-test-task
Тестовое задание "Реестр сотрудников" для компании 'Elektrik-Master'.

Стек: **FastAPI, SQLAlchemy, SQLite, Jinja2, Tailwind CSS**.



## Функциональность

- Список сотрудников с пагинацией (5 записей на страницу).
- Поиск по ФИО и телефону.
- Фильтрация по полу и возрасту.
- Добавление, редактирование, удаление сотрудников.
- Загрузка фотографии с увеличением при наведении.
- Дата рождения вместо возраста (возраст вычисляется автоматически).
- Маска ввода телефона +7(XXX)XXX-XX-XX.
- Поиск по ФИО с учетом регистра. Поиск по части ФИО работает, но без `*`.
- В форму создания \ редактирования добавлена валидация типа данных полей.
- Возраст вычисляется автоматически на основе даты рождения.
- Картинки уже лежат в Elektrik-master-test-task/backend/app/static/images. Текстовые данные надо создать самому.



## Запуск локально

### Для всех команд ниже использовался терминал `cmd`

1. Склонировать.

В локальном репозитории выполнить команды:

`git clone https://github.com/BorisMirsky/Elektrik-master-test-task.git`

`cd Elektrik-master-test-task/backend`

2. Создать виртуальное окружение и активировать его:

`python -m venv venv`

`source venv/bin/activate`  # Linux/Mac

`venv\Scripts\activate`     # Windows

3. Поставить зависимости:

`pip install -r requirements.txt`

4. В `backend/` создать файл `.env`:

`cd C:\Users\Борис\source\Elektrik-master-test-task\backend`

`echo DATABASE_URL=sqlite:///./app.db > .env`

Добавить в пустой файл строку:

`DATABASE_URL=sqlite:///./app.db`

5. Находясь в `backend/` применить миграции:

`alembic upgrade head`

6. Там же в `backend/` запустить сервер:

`uvicorn app.main:app --reload`

7. Открыть в браузере: 

`http://127.0.0.1:8000/`





## Технологии

- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM
- **SQLite** — база данных (локально)
- **Alembic** — миграции
- **Jinja2** — шаблонизатор
- **Tailwind CSS** — стилизация (через CDN)
