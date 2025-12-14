from fastapi import FastAPI
from sqlalchemy import text
from app.routers import users, curriculum, items 
from app.db import engine, Base


# Initalise tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medly AI Backend Takehome Challenge")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(curriculum.router, prefix="/lessons", tags=["curriculum"])
app.include_router(items.router, prefix="/items", tags=["items"])


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "db": "ok"}
    except Exception as err:
        return {"status": "error", "db": str(err)}
