from app.models.users import Users
from app.models.expenses import Expenses
from app.schemas.users import UserSchema, UserOutSchema, UserCreateResponse, UserLoginSchema
from app.database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.utils.security import create_password_hash, verify_password, create_token
from fastapi.security import OAuth2PasswordRequestForm




router = APIRouter(prefix="/auth")



@router.post("/register", response_model=UserCreateResponse)
def create_user(form_data: UserSchema, db:Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == form_data.username).first()
    if user is not None:
        raise HTTPException(status_code=400, detail="User already exists!")

    email = db.query(Users).filter(Users.email == form_data.email).first()
    if email is not None:
        raise HTTPException(status_code=400, detail="Email already exists!")

    password_hash = create_password_hash(form_data.password)

    user = Users(
        username = form_data.username,
        email = form_data.email,
        hashed_password = password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message" : "User created successfully",
        "data" : user
    }



@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == form_data.username).first()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Invalid credentials!")

    token = create_token({
        "sub" : str(user.id)
    })

    return{
        "access_token" : token,
        "token_type" : "bearer"
    }
