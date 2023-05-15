from fastapi import APIRouter, Depends, status, Response
from app.schemas.user import    UserCreateSchema, UserCreateResponseSchema, \
                                UserLoginSchema
from app.crud import user as user_crud
from app.schemas import user
from app.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register/", status_code=status.HTTP_201_CREATED)
def register(
        user:UserCreateSchema,
        response: Response,
        db: Session = Depends(get_db),
    ):
    user_existence = user_crud.check_user_exist(db, user)
    if user_existence:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {'msg': f'there is a user with this {user_existence}'}
    db_user = user_crud.create_user(db, user)
    response_user = UserCreateResponseSchema(
        created_at= db_user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at= db_user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return {"user": response_user.json()}


@router.post("/token/", status_code=status.HTTP_200_OK)
def token(
        user: UserLoginSchema,
        response: Response,
        db: Session = Depends(get_db),
    ):
    authenticated_user = user_crud.authenticate(db, **user.dict())
    if authenticated_user is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'msg', 'not ok'}
    return {'msg', 'ok'}
