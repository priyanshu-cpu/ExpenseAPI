from pydantic import BaseModel
from datetime import date
from users import UserOutSchema

class CategorySChema(BaseModel):
    name: str

class CategoryOutSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ExpenseSchema(BaseModel):
    title: str
    price: float
    category_id: int


class ExpenseOutSchema(BaseModel):
    id: int
    title: str
    price: float
    date: date
    category: CategoryOutSchema
    user: UserOutSchema

    class Config:
        from_attributes = True
