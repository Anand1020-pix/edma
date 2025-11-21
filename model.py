from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from .db import Base
import enum

class CategoryEnum(str, enum.Enum):
    Food = "Food"
    Transport = "Transport"
    Entertainment = "Entertainment"
    Utilities = "Utilities"
    Other = "Other"

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    salary = Column(Float, default=0.0)

    expenses = relationship("Expense", back_populates="user")


class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
    )

    expense_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="expenses")
