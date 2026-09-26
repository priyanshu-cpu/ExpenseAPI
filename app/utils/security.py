from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from pwdlib import PasswordHash
from app.settings import settings
from app.models.users import Users



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



credentials_exception = HTTPException(
    status_code=401,
    detail="Invaid or expired token!",
    headers= {"WWW-Authenticate" : "Bearer"},
)



hash_password = PasswordHash.recommended()


def create_password_hash(password):
    return hash_password.hash(password)



def verify_password(password, password_hash):
    return hash_password.verify(password, password_hash)



def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp" : expire
    })

    token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return token



def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if not payload.get("sub"):
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception



def get_current_user(payload: dict = Depends(verify_token), db:Session = Depends(get_db)):
    try:
        user_id = int(payload["sub"])
    except(ValueError, KeyError, TypeError):
        raise credentials_exception
    user = db.get(Users, user_id)

    if user is None:
        raise credentials_exception

    return user

