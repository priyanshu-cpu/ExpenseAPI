from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    username: str
    email: Optional[EmailStr]
    password: str

class UserOutSchema(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]