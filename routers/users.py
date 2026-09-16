from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from routers.auth import create_token, verify_token
from schemas.users import UserSchema, UserOutSchema

router = APIRouter(prefix ="/users")

router.post("/create", response_model=UserSchema)
def create_user(body: UserSchema, db: Session = Depends(get_db)):
    pass