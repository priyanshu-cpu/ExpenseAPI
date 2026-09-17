from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from utils.database import Base


class Users(Base):
    __tablename__ = "users"

    id =  Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True ,index=True)
    email = Column(String,unique=True, nullable= True)
    hashed_password = Column(String)


    expenses = relationship("Expenses", back_populates="user")