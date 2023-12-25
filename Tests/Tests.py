import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db, TaskCreate, TaskUpdate
from LR1 import average_age
from LR2 import find_in_different_registers
import pandas as pd
DATABASE_URL_TEST = "postgresql+psycopg:///./test.db"

engine_test = create_engine(DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


class TestAPI(unittest.TestCase):
    def setUp(self):
        # Инициализация временной базы данных для тестирования
        self.db = TestingSessionLocal()
        # Инициализация клиента для тестирования FastAPI
        self.client = TestClient(app)

    def tearDown(self):
        # Очистка базы данных после каждого теста
        self.db.close()
        # Удаление временной базы данных
        engine_test.dispose()

    def test_create_task(self):
        # Тест создания задачи
        task_data = {"task": "Test Task", "status": False}
        response = self.client.post("/tasks", json=task_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_get_task(self):
        # Тест получения задачи
        task_data = {"task": "Test Task", "status": False}
        response_create = self.client.post("/tasks", json=task_data)
        task_id = response_create.json()["id"]

        response_get = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(response_get.status_code, 200)
        self.assertIn("id", response_get.json())
        self.assertEqual(response_get.json()["id"], task_id)

    def test_update_task(self):
        # Тест обновления задачи
        task_data = {"task": "Test Task", "status": False}
        response_create = self.client.post("/tasks", json=task_data)
        task_id = response_create.json()["id"]

        task_update_data = {"task": "Updated Task", "status": True}
        response_update = self.client.put(f"/tasks/{task_id}", json=task_update_data)
        self.assertEqual(response_update.status_code, 200)
        self.assertIn("id", response_update.json())
        self.assertEqual(response_update.json()["id"], task_id)
        self.assertEqual(response_update.json()["task"], "Updated Task")
        self.assertEqual(response_update.json()["status"], True)

    def test_delete_task(self):
        # Тест удаления задачи
        task_data = {"task": "Test Task", "status": False}
        response_create = self.client.post("/tasks", json=task_data)
        task_id = response_create.json()["id"]

        response_delete = self.client.delete(f"/tasks/{task_id}")
        self.assertEqual(response_delete.status_code, 200)
        self.assertIn("message", response_delete.json())
        self.assertEqual(response_delete.json()["message"], "Task deleted")


if __name__ == "__main__":
    unittest.main()

class TestFunctions(unittest.TestCase):
    #Тест функции поиска среднего возраста
    def test_average_age(self):
        test_data = pd.DataFrame({
            'Имя': ['Иван', 'Мария', 'Петр', 'Анна'],
            'Возраст': [30, 25, 35, 28],
            'Должность': ['Разработчик', 'Аналитик', 'Разработчик', 'Менеджер']
        })
        result = average_age(test_data)
        expected_result = {'Разработчик': 32.5, 'Аналитик': 25.0, 'Менеджер': 28.0}
        self.assertEqual(result, expected_result)

#Тест функции проверки повторов с регистром
    def test_find_in_different_registers(self):
        # Тестовые данные
        test_words = ['apple', 'Orange', 'Banana', 'apple', 'Grapes']

        result = find_in_different_registers(test_words)
        expected_result = ['Orange', 'Banana', 'Grapes']
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()