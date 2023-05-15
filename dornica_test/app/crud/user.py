from sqlalchemy.orm import Session
from datetime import datetime

from app.db.models import user as user_models
from app.schemas import user as user_schemas
from app.core.security import get_password_hash, verify_password


def get_user_by_username(db: Session, username: str):
    return db.query(user_models.User).filter(user_models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_models.User).filter(user_models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_models.User).offset(skip).limit(limit).all()


def check_user_exist(db: Session, user_schemas: user_schemas.UserCreateSchema):
    if get_user_by_email(db, user_schemas.email):
        return 'email'
    if get_user_by_username(db, user_schemas.username):
        return 'username'
    return None

def create_user(db: Session, user_schemas: user_schemas.UserCreateSchema):
    hashed_password = get_password_hash(user_schemas.password1)
    db_user = user_models.User(
        full_name=user_schemas.full_name,
        username=user_schemas.username,
        email=user_schemas.email,
        password=hashed_password,
        gender=user_schemas.gender,
        BoD=user_schemas.BoD,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate(
        db: Session, 
        password: str,
        email: str|None = None, 
        username: str|None = None, 
    ) -> user_models.User|None:
    user=None
    if username:
        user = get_user_by_username(db, username=username)
    elif email:
        user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
