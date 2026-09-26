from app.models.users import Users
from app.schemas.users import UserSchema, UserOutSchema, UserCreateResponse, UserLoginSchema
from app.database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session




router = APIRouter(prefix="/auth")



@router.post("/register")
def create_user():
    pass