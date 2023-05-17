from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models import User, Listing
from app.apis.deps import get_db, get_current_related_user_listing, get_current_user
from app.core.config import settings
from app.schemas import ListingResponseSchema, ListingCreateSchema, ListingUpdateSchema
from app.crud.listing import listing_crud

router = APIRouter()


@router.get('/')
async def read_listings(
        db:     Annotated[Session, Depends(get_db)],
    ) -> list[ListingResponseSchema]:
    return listing_crud.get_multi(db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ListingResponseSchema)
async def create_listing(
        db:             Annotated[Session, Depends(get_db)],
        current_user:   Annotated[User, Depends(get_current_user)],
        listing:        ListingCreateSchema
    ):
    return listing_crud.create(db, obj_in=listing, owner_id=current_user.id)


@router.get('/{listing_id}/')
async def get_listing(
        listing_id:int, db: Annotated[Session, Depends(get_db)]
    ) -> ListingResponseSchema:
    return listing_crud.get(db, id=listing_id)


@router.put('/{listing_id}/')
async def update_listing(
        update_listing: ListingUpdateSchema,
        db: Annotated[Session, Depends(get_db)],
        authorization_result: Annotated[list[User, Listing], Depends(get_current_related_user_listing)],
    ):
    current_user, listing = authorization_result
    return listing_crud.update(db, db_obj=listing, obj_in=update_listing)


@router.delete('/{listing_id}/')
async def delete_listing(
        db: Annotated[Session, Depends(get_db)],
        authorization_result:   Annotated[list[User, Listing], Depends(get_current_related_user_listing)],
    ):
    current_user, listing = authorization_result
    listing_crud.remove(db, id=listing.id)
    return {"msg": "OK"}
