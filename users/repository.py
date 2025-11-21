from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.model import User

class UserRepository:

    async def create_user(self, db: AsyncSession, username: str, salary: float | None):
        user = User(username=username, salary=salary or 0.0)
        db.add(user)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise
        await db.refresh(user)
        return user

    async def get_user_by_id(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()
