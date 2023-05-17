import sqlalchemy

from app.crud.listing import listing_crud
from app.crud.user import user_crud
from app.models.listing import Listing
from app.tests.utils.utils import random_lower_string, random_email
from app.tests.utils.user import get_random_user, get_user_update
from app.tests.utils.listing import get_random_listing
from app.tests.utils.override import TestingSessionLocal


def test_create_listing():
    db = TestingSessionLocal()
    global_user_in = get_random_user()
    listing_schema = get_random_listing()
    user_db = user_crud.create(db, obj_in=global_user_in)
    listing_db = listing_crud.create(db, obj_in=listing_schema, owner_id=user_db.id)
    
    assert listing_db.owner_id == user_db.id
    db.close()
