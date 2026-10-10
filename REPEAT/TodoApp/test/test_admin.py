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
