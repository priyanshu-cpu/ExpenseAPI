from pydantic import BaseModel
from datetime import date
from typing import Optional

class Category(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
# class CategoryOut(BaseModel):
#     id : int

#     class Config:
#         from_attributes = True

class ExpenseBase(BaseModel):
    title : str
    price : float
    category_id : int


class ExpenseOut(BaseModel):
    id: int
    title: str
    price: float
    date: date
    category: CategoryOut

    class Config:
        from_attributes = True