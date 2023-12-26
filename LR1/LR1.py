#LR1- Работа с pandas и csv
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse





def average_age(data_cvs: pd.DataFrame) -> dict:
    try:
        # Проверка наличия необходимых столбцов
        whaiting_clumn = {'Имя', 'Возраст', 'Должность'}
        if not whaiting_clumn.issubset(data_cvs.columns):
            raise ValueError("Файл не содержит необходимых столбцов")

        # Группировка данных по должности и вычисление среднего возраста для каждой группы
        middle_age = data_cvs.groupby('Должность')['Возраст'].mean().to_dict()

        return middle_age

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))











