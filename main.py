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
#LR11- Реализация UI приложения
import pandas as pd
from fastapi import File, UploadFile, Depends
from fastapi.responses import JSONResponse
import LR1.LR1
import LR2.LR2
from sqlalchemy import create_engine, Column, String, Boolean, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import LR8.LR8

DATABASE_URL = "postgresql+psycopg://postgres:aB89027311@localhost/postgres?client_encoding=utf8"


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


