from fastapi import APIRouter, Depends
from typing import Optional
from datetime import date
from app.schemas import ExpenseCreate, ExpenseOut, TotalsOut
from app.model import CategoryEnum
from app.db import get_db
from .service import expense_service

router = APIRouter(prefix="/expenses", tags=["Expenses"], redirect_slashes=False)

@router.post("", response_model=ExpenseOut, status_code=201)
@router.post("/", response_model=ExpenseOut, status_code=201, include_in_schema=False)
async def create_expense(payload: ExpenseCreate, db=Depends(get_db)):
    return await expense_service.create_expense(db, payload)


@router.get("/{user_id}", response_model=list[ExpenseOut])
async def list_expenses(
    user_id: int,
    day: Optional[date] = None,
    week: Optional[int] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    category: Optional[CategoryEnum] = None,
    db=Depends(get_db)
):
    filters = {
        "day": day,
        "week": week,
        "month": month,
        "year": year,
        "category": category
    }
    return await expense_service.list_expenses(db, user_id, filters)


@router.get("/totals/{user_id}", response_model=TotalsOut)
async def totals(user_id: int, db=Depends(get_db)):
    return await expense_service.totals(db, user_id)
