from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from app.model import CategoryEnum

class UserCreate(BaseModel):
    username: str
    salary: Optional[float] = None

class UserOut(BaseModel):
    user_id: int
    username: str
    salary: float
    class Config:
        orm_mode = True


class ExpenseCreate(BaseModel):
    user_id: int
    name: str
    amount: float
    category: CategoryEnum

class ExpenseOut(BaseModel):
    expense_id: int
    user_id: int
    name: str
    amount: float
    category: CategoryEnum
    created_at: datetime
    class Config:
        orm_mode = True


class TotalsOut(BaseModel):
    total_expense: float
    total_salary: Optional[float]
    remaining_amount: float
    category_breakdown: Dict[str, float]
