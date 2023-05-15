from fastapi import APIRouter
from app.apis.endpoints import root, auth

api_router = APIRouter()

api_router.include_router(root.router, tags=["root"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
