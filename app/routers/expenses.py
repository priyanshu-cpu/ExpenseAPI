from app.models.expenses import Category, Expenses
from app.models.users import Users
from app.schemas.expenses import ExpenseBase, ExpenseOut, ExpenseCreateResponse
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import get_current_user, verify_token



router = APIRouter(prefix="/expense")
