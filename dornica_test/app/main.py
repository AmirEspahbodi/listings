from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.apis.api import api_router
from app.core.utils import increase_count_file

@asynccontextmanager
async def lifespan(app: FastAPI):
    increase_count_file()
    yield

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['localhost:8000', 'localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
