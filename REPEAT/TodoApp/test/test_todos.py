from urllib import response

import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from models import Todos
from main import app
from routers.auth import get_current_user

SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {
        'username': 'admin',
        'user_id': 1,
        'user_role': 'admin',
    }


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


""""
test_todo (фикстура)
    ↓
создаёт запись в тестовой БД
    ↓
test_read_all_authenticated
    ↓
client.get("/") 
    ↓
override_get_current_user → user_id=1
override_get_db → тестовая сессия
    ↓
роутер делает SELECT ... WHERE owner_id = 1
    ↓
возвращает JSON
    ↓
assert сравнивает с ожидаемым результатом
    ↓
фикстура чистит таблицу
"""

@pytest.fixture
def test_todo():
    # очистка перед тестом
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM todos;'))
        conn.commit()

    todo = Todos(
        title='learn the code',
        description='learn the description',
        priority=5,
        completed=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo

    # очистка после теста
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM todos;'))
        conn.commit()

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': test_todo.id,
        'title': 'learn the code',
        'description': 'learn the description',
        'priority': 5,
        'completed': False,
        'owner_id': 1,
    }]

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': test_todo.id,
        'title': 'learn the code',
        'description': 'learn the description',
        'priority': 5,
        'completed': False,
        'owner_id': 1,
    }

def test_read_one_authenticated_not_found():
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'todo not found'               # как в роутере
    }

def test_create_todo():
    request_data = {
        'title': 'new todo',
        'description': 'new todo desc',
        'priority': 5,
        'completed': False
    }

    response = client.post('/todos', json=request_data)   # без trailing slash
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.title == 'new todo').first()

    assert model is not None
    assert model.title == request_data['title']
    assert model.description == request_data['description']
    assert model.priority == request_data['priority']
    assert model.completed == request_data['completed']
    assert model.owner_id == 1

    # чистим за собой
    db.delete(model)
    db.commit()
    db.close()


def test_update_todo(test_todo):
    request_data = {
        'title':'change the title of the todo already saved!',
        'description': 'need to learn everyday!',
        'priority': 5,
        'completed': False
    }

    response = client.put('/todos/1', json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model.title == 'change the title of the todo already saved!'


def test_update_todo_not_found(test_todo):
    request_data = {
        'title':'change the title of the todo already saved!',
        'description': 'need to learn everyday!',
        'priority': 5,
        'completed': False
    }

    response = client.put('/todos/2', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'todo not found'}


def test_delete_todo(test_todo):
    response = client.delete('/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete('/todos/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    

