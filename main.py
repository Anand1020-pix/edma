from fastapi import FastAPI
from app.users.router import router as user_router
from app.expenses.router import router as expense_router
from app.db import engine, Base
import asyncio

app = FastAPI(redirect_slashes=False)


app.include_router(user_router)
app.include_router(expense_router)
