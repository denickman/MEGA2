from passlib import exc

from .conftest import *

from ..routers.users import get_current_user
from ..database import get_db
from ..routers.auth import authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

import pytest


def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, "test", db)

    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username


    non_existent_user = authenticate_user("WrongName", 'test', db)
    assert non_existent_user is False


    wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_password_user is False


def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(hours=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={'verify_signature': False}
    )

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {
        'sub': 'testuser',
        'id': 1,
        'role': 'admin'
    }

    token = jwt.encode(encode, SECRET_KEY, algorithm='HS256')

    user = await get_current_user(token=token)

    assert user == {
        'username': 'testuser',
        'user_id': 1,
        'user_role': 'admin'
    }


@pytest.mark.asyncio
async def test_get_current_user_missiong_payload():
    encode = {
        'role': 'user'
    }
    token = jwt.encode(encode, SECRET_KEY, algorithm='HS256')

    with pytest.raises(HTTPException) as exinfo:
        await get_current_user(token=token)

    assert exinfo.value.status_code == 401
    assert exinfo.value.detail == 'Invalid Credentials'















