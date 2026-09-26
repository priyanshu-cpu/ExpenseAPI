from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db