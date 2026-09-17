from jose import jwt, JWTError
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from utils.settings import settings
from utils.database import get_db
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from models.users import Users
from utils.database import get_db
from utils.settings import settings


bearer_scheme = HTTPBearer(bearerFormat="JWT")

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token!",
    headers={"WWW-Authenticate" : "Bearer"},
)

hash_password = PasswordHash.recommended()

def get_password_hash(password):
    return hash_password.hash(password)

def verify_password(password, hashed_password):
    return hash_password.verify(password,hashed_password)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp" : expire
    })

    token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return token

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if not payload.get("sub"):
            raise credential_exception
        return payload
    except JWTError:
        raise credential_exception

def get_current_user(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        user_id = int(payload["sub"])
    except (KeyError,TypeError, ValueError):
        raise credential_exception
    user = db.get(Users, user_id)

    if user is None:
        raise credential_exception

    return user