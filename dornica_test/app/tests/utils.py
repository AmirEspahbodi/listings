import random
import string
from datetime import date

from app.schemas import UserCreateSchema
from app.models.user import GenderEnum


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))

def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"

def random_date() -> date:
    return date(
        year=random.randrange(1900, 2023, 1),
        month=random.randrange(1, 12, 1) ,
        day=random.randrange(1, 29, 1))

def get_random_user():
    pwd = random_lower_string()
    return UserCreateSchema(
        username=   random_lower_string(),
        full_name=  random_lower_string(),
        email=      random_email(),
        password1=  pwd,
        password2=  pwd,
        gender=     GenderEnum.MAIL,
        BoD=        random_date()
    )

def get_serializable_random_user():
    user_in = get_random_user().dict()
    user_in['BoD']=user_in.get('BoD').strftime("%Y-%m-%d")
    user_in['gender'] = user_in.get('gender').name
    return user_in
