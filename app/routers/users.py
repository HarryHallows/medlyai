from fastapi import APIRouter

from app.schemas import UserOut


router = APIRouter()

@router.get("/{id}", response_model=UserOut)
def get_user(id: str):
    pass
