import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "app/static/images"

def ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(file: UploadFile) -> str:
    # Сохраняет загруженный файл в папку uploads. Возвращает относительный URL для доступа к файлу.
    ensure_upload_dir()
    
    # Генерируем уникальное имя, чтобы избежать конфликтов
    file_extension = os.path.splitext(file.filename)[1]  # .jpg, .png и т.д.
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        content = await file.read()  # асинхронно читаем
        buffer.write(content)
    
    # Возвращаем URL, по которому файл будет доступен из браузера
    return f"/static/images/{unique_filename}"