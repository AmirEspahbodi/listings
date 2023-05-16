from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import UserCreateSchema, UserCreateResponseSchema, \
                        UserSchema, UserUpdateSchema, UserChangePasswordSchema
from app.models import User
from app.core.security import create_access_token
from app.crud.user import user_crud, check_user_exist
from app.apis.deps import get_db, get_current_related_user, get_current_user
from app.core.config import settings

router = APIRouter()


@router.post("/register/", summary="Create new user", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponseSchema)
def register(
        db:     Annotated[Session, Depends(get_db)],
        user:   UserCreateSchema,
    ):
    user_existence = check_user_exist(db, username=user.username, email=user.email)
    if user_existence:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'there is a user with this {user_existence}'
        )  
    db_user = user_crud.create(db, obj_in=user)
    
    return {
        'created_at' : db_user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        'updated_at' : db_user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }


@router.post("/token", summary="Create access and refresh tokens for user", status_code=status.HTTP_200_OK)
def token(
        # user: UserLoginSchema,
        db: Annotated[Session, Depends(get_db)],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ):
    authenticated_user = user_crud.authenticate(db, username=form_data.username, password=form_data.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='The username or password is incorrect'
        )
    return {
        "access_token":     create_access_token(data={"sub": authenticated_user.username}),
        "refresh_token":    create_access_token(data={"sub": authenticated_user.username}, refresh=True)
    }


@router.get('/me/@{username}/', summary='Get details of currently logged in user', response_model=UserSchema)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_related_user)]
    ):
    return current_user


@router.put('/me/@{username}/', summary='update currently logged in user information', response_model=UserSchema)
async def update_users_me(
        db: Annotated[Session, Depends(get_db)],
        update_info: UserUpdateSchema,
        current_user: Annotated[User, Depends(get_current_related_user)],
    ):
    user_existence_result = check_user_exist(db, username=update_info.username, email=update_info.email)
    if  user_existence_result and update_info.username != user_existence_result.get('exist_obj').username or \
        settings.DB_EMAIL_UNIQUE and update_info.email != user_existence_result.get('exist_obj').email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"there is a user with this {user_existence_result.get('field')}"
        )
    if update_info.password:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='can not change password through this endpoint'
        )
    current_user = user_crud.update(db, db_obj=current_user, obj_in=update_info)
    return current_user
