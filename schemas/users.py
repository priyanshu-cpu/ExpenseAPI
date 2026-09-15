from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    username: str
    email: Optional[EmailStr] = None 
    password: str

class UserOutSchema(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None 

    class Config:
        from_attributes = True
