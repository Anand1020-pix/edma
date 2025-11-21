from sqlalchemy.ext.asyncio import AsyncSession
from app.model import User

class UserRepository:

    async def create_user(self, db: AsyncSession, username: str, salary: float | None):
        user = User(username=username, salary=salary or 0.0)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
