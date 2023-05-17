from datetime import date, datetime
from pydantic import BaseModel, constr, EmailStr, root_validator
from app.models.user import GenderEnum


class UserBaseSchema(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    gender: GenderEnum = GenderEnum.NOT_SPECIFIED
    BoD: date


class FullUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    created_at: datetime
    updated_at: datetime


class UserCreateSchema(UserBaseSchema):
    password1: constr(min_length=8)
    password2: constr(min_length=8)
    
    @root_validator
    def check_passwords_match(cls, values):
        pw1, pw2 = values.get('password1'), values.get('password2')
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return values


class UserSchema(UserBaseSchema):
    id: int
    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    username: str|None = None
    full_name: str|None = None
    email: EmailStr|None = None
    gender: GenderEnum|None = None
    password: str|None = None
    BoD: date|None = None


class UserChangePasswordSchema(BaseModel):
    password1: constr(min_length=8)
    password2: constr(min_length=8)
    @root_validator
    def check_passwords_match(cls, values):
        pw1, pw2 = values.get('password1'), values.get('password2')
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return values


class UserCreateResponseSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
