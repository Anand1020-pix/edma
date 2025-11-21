from fastapi import APIRouter, Depends
from app.schemas import UserCreate, UserOut
from app.db import get_db
from .service import user_service

router = APIRouter(prefix="/users", tags=["Users"], redirect_slashes=False)

@router.post("", response_model=UserOut, status_code=201)
@router.post("/", response_model=UserOut, status_code=201, include_in_schema=False)
async def create_user(payload: UserCreate, db=Depends(get_db)):
    return await user_service.create_user(db, payload)
