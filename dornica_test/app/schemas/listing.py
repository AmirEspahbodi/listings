from datetime import datetime

from pydantic import BaseModel

from app.models.listing import ListingTypeEnum


class ListingBaseschema(BaseModel):
    type: ListingTypeEnum
    available_now: bool = True
    address: str


class ListingCreateSchema(ListingBaseschema):
    pass


class ListingUpdateSchema(ListingBaseschema):
    type: ListingTypeEnum|None = None
    available_now: bool|None = None
    address: str|None = None


class ListingSchema(ListingBaseschema):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ListingFullSchema(ListingBaseschema):
    owner_id:   int
    created_at: datetime
    updated_at: datetime


class ListingResponseSchema(ListingBaseschema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
