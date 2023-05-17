from typing import Dict
from datetime import datetime

from fastapi.testclient import TestClient

from app.tests.utils.utils import random_email, random_lower_string, random_date
from app.schemas import ListingCreateSchema
from app.models.listing import ListingTypeEnum
from app.core.config import settings

def get_random_listing():
    return ListingCreateSchema(
        address=random_lower_string(),
        available_now=True,
        type=ListingTypeEnum.APARTMENT
    )