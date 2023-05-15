from fastapi import FastAPI
from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware
from app.apis.api import api_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['localhost:8000', 'localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
