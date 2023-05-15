from app.crud import user as user_crud
from app.tests.utils import random_lower_string, get_random_user
from app.tests.override import TestingSessionLocal


def test_create_user():
    db = TestingSessionLocal()
    user_in = get_random_user()
    user = user_crud.create_user(db, user_schemas=user_in)
    db.close()
    assert user.email == user_in.email
    assert user.username == user_in.username
    assert hasattr(user, "password")


def test_authenticate_user() -> None:
    db = TestingSessionLocal()
    user_in = get_random_user()
    user = user_crud.create_user(db, user_schemas=user_in)
    authenticated_user_username = user_crud.authenticate(db, username=user.username, password=user_in.password1)
    db.close()
    assert authenticated_user_username
    assert user.email==authenticated_user_username.email
    assert user.username==authenticated_user_username.username


def test_not_authenticate_user() -> None:
    db = TestingSessionLocal()
    username = random_lower_string()
    password = random_lower_string()
    user = user_crud.authenticate(db, username=username, password=password)
    db.close()
    assert user is None
