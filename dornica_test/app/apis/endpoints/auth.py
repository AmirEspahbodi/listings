from typing import Annotated
from fastapi import APIRouter, Depends, status, Response, HTTPException
from app.schemas.user import    UserCreateSchema, UserCreateResponseSchema, \
                                UserLoginSchema, UserSchema
from app.core.security import create_access_token, create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm
from app.crud import user as user_crud
from app.apis.deps import get_db
from sqlalchemy.orm import Session
from app.apis.deps import get_current_user

router = APIRouter()


@router.post("/register/", summary="Create new user", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponseSchema)
def register(
        user:UserCreateSchema,
        db: Annotated[Session, Depends(get_db)],
    ):
    user_existence = user_crud.check_user_exist(db, user)
    if user_existence:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'there is a user with this {user_existence}'
        )
    db_user = user_crud.create_user(db, user)
    
    return {
        'created_at' : db_user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        'updated_at' : db_user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }


@router.post("/token/", summary="Create access and refresh tokens for user", status_code=status.HTTP_200_OK)
def token(
        # user: UserLoginSchema,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
    ):
    print(form_data.username, form_data.password)
    authenticated_user = user_crud.authenticate(db, username=form_data.username, password=form_data.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='The username or password is incorrect'
        )
    return {
        "access_token":     create_access_token(authenticated_user.username),
        "refresh_token":    create_refresh_token(authenticated_user.username),
    }


@router.get('/me', summary='Get details of currently logged in user')
async def get_me(user: Annotated[UserSchema, Depends(get_current_user)]):
    return user