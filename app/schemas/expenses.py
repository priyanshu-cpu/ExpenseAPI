from pydantic import BaseModel, Field, ConfigDict
from datetime import date as Date


class CategoryBase(BaseModel):
    name: str


class CategoryOut(BaseModel):
    id: int
    name : str

    model_config = ConfigDict(from_attributes=True)

class CategoryCreateResponse(BaseModel):
    message : str
    data : CategoryOut



class ExpenseBase(BaseModel):
    title: str
    amount: int
    category_id: int

class ExpenseOut(BaseModel):
    id: int
    title: str
    amount: int
    date: Date | None  = None
    category: CategoryOut

    model_config = ConfigDict(from_attributes=True)


class ExpenseCreateResponse(BaseModel):
    message: str
    data: ExpenseOut