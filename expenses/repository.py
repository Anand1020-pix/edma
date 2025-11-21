from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from app.model import Expense, User

class ExpenseRepository:

    async def create_expense(self, db: AsyncSession, data):
        expense = Expense(**data)
        db.add(expense)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise
        await db.refresh(expense)
        return expense

    async def get_expenses(self, db: AsyncSession, user_id: int, filters: dict):
        query = select(Expense).where(Expense.user_id == user_id)

        if filters.get("day"):
            query = query.filter(func.date(Expense.created_at) == filters["day"])

        if filters.get("week") and filters.get("year"):
            query = query.filter(
                func.extract("week", Expense.created_at) == filters["week"],
                func.extract("year", Expense.created_at) == filters["year"],
            )

        if filters.get("month") and filters.get("year"):
            query = query.filter(
                func.extract("month", Expense.created_at) == filters["month"],
                func.extract("year", Expense.created_at) == filters["year"],
            )

        if filters.get("category"):
            query = query.filter(Expense.category == filters["category"])

        result = await db.execute(query)
        return result.scalars().all()

    async def get_totals(self, db: AsyncSession, user_id: int):
        # total expense
        total_expense = await db.scalar(
            select(func.coalesce(func.sum(Expense.amount), 0)).where(Expense.user_id == user_id)
        )

        # salary
        salary = await db.scalar(
            select(User.salary).where(User.user_id == user_id)
        )

        # category sum
        stmt = select(Expense.category, func.sum(Expense.amount)).where(
            Expense.user_id == user_id
        ).group_by(Expense.category)

        rows = (await db.execute(stmt)).all()

        category_breakdown = {str(cat): float(amt) for cat, amt in rows}

        return {
            "total_expense": float(total_expense or 0),
            "total_salary": float(salary or 0),
            "remaining_amount": float((salary or 0) - (total_expense or 0)),
            "category_breakdown": category_breakdown
        }
