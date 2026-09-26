from pydantic import BaseModel, Field, ConfigDict


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


class ExpenseOut(BaseModel):
    id: int
    title: str
    amount: int

    model_config = ConfigDict(from_attributes=True)


class ExpenseCreateResponse(BaseModel):
    message: str
    data: ExpenseOut