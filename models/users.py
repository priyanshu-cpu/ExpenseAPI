from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from utils.database import Base


class Users(Base):
    __tablename__ = "users"

    id =  Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, nullable= True)
    hashed_password = Column(String)


    expenses = relationship("Expenses", back_populates="user")