from typing import Any

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def read_items() -> Any:
    return {"msg": "hello"}