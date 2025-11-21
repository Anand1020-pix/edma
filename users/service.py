from sqlalchemy.ext.asyncio import AsyncSession
from .repository import UserRepository

user_repo = UserRepository()

class UserService:

    async def create_user(self, db: AsyncSession, payload):
        return await user_repo.create_user(db, payload.username, payload.salary)

user_service = UserService()
