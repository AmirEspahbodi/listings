from typing import Generator, Annotated
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import SessionLocal
from app.schemas import TokenData
from app.crud.user import user_crud
from app.crud.listing import listing_crud
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = user_crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_related_user(
    username:str,
    current_user: Annotated[User, Depends(get_current_user)]
):
    if (username != current_user.username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='access denied!'
        )
    return current_user


async def get_current_related_user_listing(
    listing_id:int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    listing = listing_crud.get(db, listing_id)
    if (listing.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='access denied!'
        )
    return current_user, listing
