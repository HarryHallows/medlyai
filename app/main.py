from fastapi import FastAPI
from sqlalchemy import text
from app.routers import health, users, curriculum, items 
from app.db import engine, Base


# Initalise tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medly AI Backend Takehome Challenge")

app.include_router(health.router)
app.include_router(users.router)
app.include_router(curriculum.router)
app.include_router(items.router)
