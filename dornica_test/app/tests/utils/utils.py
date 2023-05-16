import random
import string
from datetime import date


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))

def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()[:7]}.com"

def random_date() -> date:
    return date(
        year=random.randrange(1900, 2023, 1),
        month=random.randrange(1, 12, 1) ,
        day=random.randrange(1, 29, 1))
