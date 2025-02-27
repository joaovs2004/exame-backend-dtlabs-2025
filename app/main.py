from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.session import create_db_and_tables

from .routers import auth, data, health, servers

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(data.router)
app.include_router(health.router)
app.include_router(servers.router)
