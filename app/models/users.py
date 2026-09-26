from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id =  Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True ,index=True)
    email = Column(String,unique=True, nullable= True)
    hashed_password = Column(String)

    category = relationship("Category", back_populates="user")
    expenses = relationship("Expenses", back_populates="user")