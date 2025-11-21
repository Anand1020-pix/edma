from .repository import ExpenseRepository

expense_repo = ExpenseRepository()

class ExpenseService:

    async def create_expense(self, db, payload):
        return await expense_repo.create_expense(db, payload.dict())

    async def list_expenses(self, db, user_id, filters):
        return await expense_repo.get_expenses(db, user_id, filters)

    async def totals(self, db, user_id):
        return await expense_repo.get_totals(db, user_id)

expense_service = ExpenseService()
