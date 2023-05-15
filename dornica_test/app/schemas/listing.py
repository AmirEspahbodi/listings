from datetime import datetime

from pydantic import BaseModel

from app.models.listing import ListingTypeEnum

class ListingBaseschema(BaseModel):
    type: ListingTypeEnum
    available_now: bool = True
    address: str
    created_at: datetime
    updated_at: datetime

class ListingCreateschema(ListingBaseschema):
    pass

class Listingschema(ListingBaseschema):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
