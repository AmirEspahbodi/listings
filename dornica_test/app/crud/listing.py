from datetime import datetime

from sqlalchemy.orm import Session, defer, undefer

from app.crud.base import CRUDBase
from app.models.listing import Listing
from app.schemas.listing import ListingCreateSchema, ListingUpdateSchema, ListingFullSchema


class CRUDListing(CRUDBase[Listing, ListingCreateSchema, ListingUpdateSchema]):
    def create(self, db: Session, *, obj_in: ListingCreateSchema, owner_id: int) -> Listing:
        fullSchema = ListingFullSchema(
            **obj_in.dict(),
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow(),
            owner_id=owner_id
        )
        return super().create(db, obj_in=fullSchema)

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> list[Listing]:
        return db.query(self.model).filter(Listing.owner_id == owner_id).offset(skip).limit(limit).all()


listing_crud = CRUDListing(Listing)