from app.crud import user as user_crud
from app.tests.utils.utils import random_email, random_lower_string, random_date, get_random_user
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
    authenticated_user_email = user_crud.authenticate(db, email=user.email, password=user_in.password1)
    authenticated_user_username = user_crud.authenticate(db, username=user.username, password=user_in.password1)
    db.close()
    assert authenticated_user_email
    assert authenticated_user_username
    assert user.email == authenticated_user_email.email and user.email==authenticated_user_username.email
    assert user.username == authenticated_user_email.username and user.username==authenticated_user_username.username


def test_not_authenticate_user() -> None:
    db = TestingSessionLocal()
    email = random_email()
    password = random_lower_string()
    user = user_crud.authenticate(db, email=email, password=password)
    db.close()
    assert user is None
