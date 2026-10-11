from .conftest import *

from fastapi import status
from database import get_db
from routers.auth import get_current_user
from main import app

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [{
        'completed'  : False,
        'title' : 'learn the code',
        'description' : 'learn the description',
        'id': 1,
        'priority' : 5,
        'owner_id': 1
    }]


def test_admin_delete_todo(test_todo):
    response = client.delete('/admin/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None



def test_admin_delete_todo_not_found():
    response = client.delete('/admin/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'todo not found'
    }













