from sqlalchemy.orm import Session
from datetime import datetime

from app.models import User
from app.schemas import UserCreateSchema
from app.core.security import get_password_hash, verify_password


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def check_user_exist(db: Session, user_schemas: UserCreateSchema):
    if get_user_by_username(db, user_schemas.username):
        return 'username'
    return None


def create_user(db: Session, user_schemas: UserCreateSchema):
    hashed_password = get_password_hash(user_schemas.password1)
    db_user = User(
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
        username: str, 
    ) -> User|None:
    '''
    return user if username and password are correct
    return False if user exist with this username but password is incorrext
    return None if user does not exist witth this username
    '''
    user= get_user_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return False
    return user
