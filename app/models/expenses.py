from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date


class Category(Base):
    __tablename__ = "categories"

    id  = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable= False)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", back_populates="category")
    expenses = relationship("Expenses", back_populates="category")


class Expenses(Base):
    __tablename__ = "expenses"

    id  = Column(Integer, primary_key=True, index=True)
    title  = Column(String)
    amount  = Column(Integer)
    date  = Column(Date, default=date.today)


    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)


    category = relationship("Category", back_populates="expenses")
    user = relationship("Users", back_populates="expenses")