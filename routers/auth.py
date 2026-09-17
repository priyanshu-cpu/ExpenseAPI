from jose import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from utils.settings import settings
from utils.database import get_db
from fastapi import HTTPException, status
from pwdlib import PasswordHash

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

def verify_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token!")

