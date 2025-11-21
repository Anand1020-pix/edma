from fastapi import FastAPI
from app.users.router import router as user_router
from app.expenses.router import router as expense_router
from app.db import engine, Base
import asyncio

app = FastAPI(redirect_slashes=False)

# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

app.include_router(user_router)
app.include_router(expense_router)
