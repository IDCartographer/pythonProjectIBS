#Данный проект/репозиторий создан в рамках стажировки
#В рамках проекта все задания имеют следующие обозначения:
#LR1- Работа с pandas и csv
#LR2- Фильтрация массива с учетом регистра строки
#LR3- Реализация API для хранения и управления данными
#LR4- Работа с PostgreSQL и SQLAlchemy
#LR5- Тестирование
#LR6- Контейнеризация приложения
#LR7- Цепное суммирование
#LR8- Конвертер из integer в Римские цифры
#LR9- API для хранения файлов
#LR10- Генерация файлов в форматах CSV, JSON и YAML
#LR11- Логирование в FastAPI с использованием middleware
#LR12- Реализация UI приложения
import pandas as pd
from fastapi import File, UploadFile, Depends
from fastapi.responses import JSONResponse
import LR1.LR1
import LR2.LR2
from sqlalchemy import create_engine, Column, String, Boolean, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel
import LR8.LR8
from fastapi.responses import FileResponse
from datetime import datetime
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import os
import zipfile
import uuid
from starlette.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse


DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost/postgres?client_encoding=utf8"




engine = create_engine(DATABASE_URL, client_encoding='UTF-8')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
#описание запроса
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)
    status = Column(Boolean, default=False)
Base.metadata.create_all(bind=engine)
#Обновление данных
class TaskUpdate(BaseModel):
    task: str
    status: bool

#Создание запроса
class TaskCreate(BaseModel):
    task: str
    status: bool = False
#Ответ на запрос
class TaskResponse(BaseModel):
    id: int
    task: str
    status: bool
#Получение БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
app=FastAPI()

UPLOAD_FOLDER = 'uploads'

app.config = {'UPLOAD_FOLDER': UPLOAD_FOLDER}


def allowed_file(filename):
    return '.' in filename
#LR1-average_age_by_position 1.2
@app.post("/average_age_by_position")
async def average_age_by_position(file: UploadFile = File(...)) -> JSONResponse:
    try:
        # Чтение данных из CSV файла в DataFrame
        DataFrame = pd.read_csv(file.file)

        # Вызов функции и возврат результата
        result = LR1.LR1.average_age(DataFrame)
        return JSONResponse(content=result)

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Ошибка: Файл пуст")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Ошибка: Некорректный формат файла")
#LR1- End method

#LR2-find_in_different_registers 2.2
@app.post("/reg_filter")
async def find_in_different_registers(words: list[str])-> JSONResponse:
    try:
        result= LR2.LR2.find_in_different_registers(words)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
#LR2- End method

#LR3- Реализация API для хранения и управления данными
#LR4- Работа с PostgreSQL и SQLAlchemy
@app.post("/tasks", response_model=dict)
async def create_task(task: TaskCreate):
    db_task = Task(**task.dict())
    with SessionLocal() as session:
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
    return {"id": db_task.id, **task.dict()}

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Создаем экземпляр Pydantic-модели только с нужными полями
    task_response = TaskResponse(id=task.id, task=task.task, status=task.status)
    return task_response.dict()
@app.put("/tasks/{task_id}", response_model=dict)
async def update_task(task_id: int, task: TaskUpdate):
    with SessionLocal() as session:
        db_task = session.query(Task).filter(Task.id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        for key, value in task.dict().items():
            setattr(db_task, key, value)

        session.commit()
        return {"id": task_id, **task.dict()}


@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    with SessionLocal() as session:
        db_task = session.query(Task).filter(Task.id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(db_task)
        session.commit()
        return {"message": "Task deleted"}

#LR3,4 END

#LR8 Конвертер из integer в Римские цифры
@app.post("/int_to_roman")
def convert_to_roman(number: int) -> str:
    if not 1 <= number <= 3999:
        raise HTTPException(status_code=400, detail="Number must be between 1 and 3999")
    roman_num = LR8.LR8.int_to_roman(number)
    return roman_num

print(LR8.LR8.int_to_roman(5))
#LR8 end
#LR9 API для хранения файлов
#имеется проблема, файл то он сохраняет, но не сохраняет формат файла. Хотя при открытии все данные впорядке
@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...), archive: bool = Form(False)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_id)

    with open(file_path, "wb") as f:
        f.write(file.file.read())
    if archive:
        with zipfile.ZipFile(file_path + '.zip', 'w') as zip_file:
            zip_file.write(file_path, os.path.basename(file_path))
        os.remove(file_path)

        return {'file_id': file_id, 'archived': True}
    else:
        return {'file_id': file_id, 'archived': False}


@app.get("/download_file/{file_id}")
async def download_file(file_id: str):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    if os.path.exists(file_path + '.zip'):
        return StreamingResponse(open(file_path + '.zip', 'rb'), media_type='application/zip',
                                  headers={"Content-Disposition": f"attachment; filename={file_id}.zip"})
    else:
        return FileResponse(file_path, media_type='application/octet-stream',
                            headers={"Content-Disposition": f"attachment; filename={file_id}"})

#LR9 END


#LR11 Логирование в FastAPI с использованием middleware

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)-8s - | %(message)s |",
    datefmt="%Y-%m-%d %H:%M:%S"
)



class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Время начала выполнения запроса
        start_time = datetime.utcnow()

        async def _send(message):
            if message["type"] == "http.response.start":
                # Время окончания выполнения запроса
                end_time = datetime.utcnow()
                execution_time_sec = (end_time - start_time).total_seconds()
                # Логирование информации о запросе
                logging.info(
                    f"[{end_time}] {scope.get('file') or 'unknown'}:{scope.get('line') or 'unknown'} "
                    f"{message['status']} | {execution_time_sec:.2f} | {scope['method']} | {scope['path']}"
                )

            return await send(message)

        return await self.app(scope, receive, _send)


app.add_middleware(LoggingMiddleware)

#LR11 end


#LR12 UI
templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
#end