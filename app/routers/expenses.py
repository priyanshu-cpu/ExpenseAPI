from app.models.expenses import Category, Expenses
from app.models.users import Users
from app.schemas.expenses import CategoryBase, CategoryOut, CategoryCreateResponse
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db


router = APIRouter(prefix="/category")