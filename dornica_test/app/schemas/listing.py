from datetime import datetime

from pydantic import BaseModel

from app.db.models.enum_types import ListingTypeEnum

class ListingBase(BaseModel):
    type: ListingTypeEnum
    available_now: bool = True
    address: str
    created_at: datetime
    updated_at: datetime


class ListingCreate(ListingBase):
    pass


class Listing(ListingBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
