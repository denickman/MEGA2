from .conftest import *
from ..routers.users import get_current_user
from ..database import get_db

from fastapi import status

def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'admin'
    assert response.json()['first_name'] == 'admin'
    assert response.json()['email'] == 'admin@gmail.com'
    assert response.json()['first_name'] == 'admin'
    # etc...



def test_change_password_success(test_user):
    response = client.put('/user/change_password', json = { 'password': 'test', 'new_password': 'new_test' })
    assert response.status_code == status.HTTP_204_NO_CONTENT



def test_change_password_invalid_current_password(test_user):
    response = client.put(
        '/user/change_password',
        json={'password': 'wrong_password', 'new_password': 'new_test'}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Error on password change'


def test_change_phone_number_success(test_user):
    response = client.put('/user/phone_number/12345')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    user = db.query(Users).filter(Users.id == 1).first()
    assert user.phone_number == '12345'











