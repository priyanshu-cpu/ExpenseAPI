from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from utils.database import get_db
from routers.auth import create_token, verify_token, get_password_hash, verify_password
from schemas.users import UserSchema, UserOutSchema, UserCreateResponse
from models.users import Users

router = APIRouter(prefix ="/users")

@router.post("/create", response_model=UserCreateResponse)
def create_user(body: UserSchema, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == body.username).first()
    if user is not None:
        print(user)
        raise HTTPException(status_code=400, detail="User already exists!")

    email = db.query(Users).filter(Users.email == body.email).first()
    if email is not None:
        raise HTTPException(status_code=400, detail="Email already exists!")

    hash_password = get_password_hash(body.password)

    db_user = Users(username = body.username,
                     email = body.email,
                     hashed_password = hash_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return{
        "message" : "user created successfully",
        "data" : db_user
    }