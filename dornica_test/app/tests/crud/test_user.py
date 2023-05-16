from app.crud.user import user_crud
from app.tests.utils.utils import random_lower_string, random_email
from app.tests.utils.user import get_random_user, get_user_update
from app.tests.utils.override import TestingSessionLocal

# --------
global_user_in = get_random_user()
def test_create_user():
    db = TestingSessionLocal()
    user = user_crud.create(db, obj_in=global_user_in)
    db.close()
    assert user.email == global_user_in.email
    assert user.username == global_user_in.username
    assert hasattr(user, "password")


def test_authenticate_user() -> None:
    db = TestingSessionLocal()
    authenticated_user_username = user_crud.authenticate(db, username=global_user_in.username, password=global_user_in.password1)
    db.close()
    assert authenticated_user_username
    assert global_user_in.email==authenticated_user_username.email
    assert global_user_in.username==authenticated_user_username.username


def test_not_authenticate_user() -> None:
    db = TestingSessionLocal()
    password = random_lower_string()
    user = user_crud.authenticate(db, username=global_user_in.username, password=password)
    db.close()
    assert not user
# --------


def test_update_user_email() -> None:
    db = TestingSessionLocal()
    user_in = get_random_user()
    db_user_in = user_crud.create(db, obj_in=user_in)
    update_user_in = get_user_update(email=random_email())
    db_updated_user = user_crud.update(db, db_obj=db_user_in, obj_in=update_user_in)
    db.close()
    assert db_updated_user is not None
    assert db_updated_user.email != user_in.email
    assert db_updated_user.username == user_in.username


def test_update_user_username() -> None:
    db = TestingSessionLocal()
    user_in = get_random_user()
    db_user_in = user_crud.create(db, obj_in=user_in)
    update_user_in = get_user_update(username=random_lower_string())
    db_updated_user = user_crud.update(db, db_obj=db_user_in, obj_in=update_user_in)
    db.close()
    assert db_updated_user is not None
    assert db_updated_user.email == user_in.email
    assert db_updated_user.username != user_in.username


def test_update_user_password() -> None:
    db = TestingSessionLocal()
    user_in = get_random_user()
    db_user_in = user_crud.create(db, obj_in=user_in)
    
    new_password=random_lower_string()
    update_user_in = get_user_update(password=new_password)
    db_updated_user = user_crud.update(db, db_obj=db_user_in, obj_in=update_user_in)
    
    authenticated_user_username = user_crud.authenticate(
        db, password=new_password, username=db_updated_user.username)
    
    db.close()
    assert db_updated_user is not None
    assert db_updated_user.email == user_in.email
    assert db_updated_user.username == user_in.username
    assert authenticated_user_username.username == user_in.username

