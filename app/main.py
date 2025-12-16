from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import curriculum_and_assessments, health, users
from app.db import engine, Base


@asynccontextmanager
async def startup_lifespan(app: FastAPI):
    # Initalise tables
    Base.metadata.create_all(bind=engine)

    yield

    engine.dispose()

app = FastAPI(lifespan=startup_lifespan)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(curriculum_and_assessments.router)
