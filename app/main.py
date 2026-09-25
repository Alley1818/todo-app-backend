from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.task import router as task_router
from app.db.session import engine
from app.models.base import Base


@asynccontextmanager
async def lifespan(_: FastAPI):
    await run_in_threadpool(Base.metadata.create_all, bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)