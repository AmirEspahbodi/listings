from datetime import datetime

from typing import Any, Dict
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas import UserCreateSchema, UserUpdateSchema
from app.core.config import settings


class CRUDUser(CRUDBase[User, UserCreateSchema, UserUpdateSchema]):
    def create(self, db: Session, *, obj_in: UserCreateSchema) -> User:
        hashed_password = get_password_hash(obj_in.password1)
        db_user = User(
            full_name=obj_in.full_name,
            username=obj_in.username,
            email=obj_in.email,
            password=hashed_password,
            gender=obj_in.gender,
            BoD=obj_in.BoD,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdateSchema|Dict[str, Any]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get('password'):
            update_data["password"] = get_password_hash(update_data["password"])
        update_data["updated_at"] = datetime.utcnow()
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_user(self, db: Session, *, username: str|None=None, email: str|None=None):
        return  db.query(User).filter(User.username == username).first() if username else \
                db.query(User).filter(User.email == email).first() if email else \
                None

    def authenticate(self, db: Session, *, password: str, username: str) -> User|None:
        '''
        return user if username and password are correct
        return False if user exist with this username but password is incorrext
        return None if user does not exist witth this username
        '''
        user= self.get_user(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return False
        return user
    
user_crud = CRUDUser(User)

def check_user_exist(db: Session, username: str, email: str|None=None):
    user_existenc = db.query(User).filter(User.username == username).first()
    if user_existenc:
        return {'exist_obj':user_existenc, 'field':'username'}
    if settings.DB_EMAIL_UNIQUE:
        user_existenc = db.query(User).filter(User.email == email).first()
        if user_existenc:
            return {'exist_obj':user_existenc, 'field':'email'}
    return None
