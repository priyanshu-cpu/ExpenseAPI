from pydantic import BaseModel
from datetime import date

class Category(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class Expense(BaseModel):
    title: str
    price: float
    category_id: int


class ExpenseOut(BaseModel):
    id: int
    title: str
    price: float
    date: date
    category: CategoryOut

    class Config:
        from_attributes = True
