from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.users.repository import UserRepository
from .repository import ExpenseRepository

expense_repo = ExpenseRepository()
user_repo = UserRepository()

class ExpenseService:

    async def create_expense(self, db, payload):
        # Ensure user exists before creating an expense to avoid FK violation
        user_exists = await user_repo.get_user_by_id(db, payload.user_id)
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        try:
            return await expense_repo.create_expense(db, payload.dict())
        except IntegrityError:
            # Safeguard in case of race condition or other constraint errors
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expense data")

    async def list_expenses(self, db, user_id, filters):
        return await expense_repo.get_expenses(db, user_id, filters)

    async def totals(self, db, user_id):
        return await expense_repo.get_totals(db, user_id)

expense_service = ExpenseService()
