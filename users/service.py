from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from .repository import UserRepository

user_repo = UserRepository()

class UserService:

    async def create_user(self, db: AsyncSession, payload):
        try:
            return await user_repo.create_user(db, payload.username, payload.salary)
        except IntegrityError:
            # surface unique constraint violations as client error
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

user_service = UserService()
