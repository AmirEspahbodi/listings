# migrations
import os
migrations = 'alembic revision --autogenerate -m "New Migration"'
migrate = 'alembic upgrade head'
os.system(migrations)
os.system(migrate)

# add 3 user to db
from app.tests.utils.user import get_random_user
from app.db.database import SessionLocal
from app.crud import user_crud
db = SessionLocal()
users = [
    user_crud.create(db, obj_in=get_random_user()) for i in range(0, 3)
]
db.close()
