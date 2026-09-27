from app.models.expenses import Category, Expenses
from app.models.users import Users
from app.schemas.expenses import ExpenseBase, ExpenseOut, ExpenseCreateResponse
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import get_current_user, verify_token



router = APIRouter(prefix="/expense")



@router.get("/get", response_model=list[ExpenseOut])
def list_expense(db:Session = Depends(get_db), user:Users = Depends(get_current_user)):
    expense = db.query(Expenses).filter(Expenses.user_id == user.id).all()
    if not expense:
        raise HTTPException(status_code=404, detail="No expense found")

    return expense



@router.get("/get/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, db:Session = Depends(get_db), user: Users = Depends(get_current_user)):
    expense = db.query(Expenses).filter(Expenses.id == expense_id, Expenses.user_id == user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Not found!")

    return expense



@router.post("/create", response_model=ExpenseCreateResponse)
def create_expense(form_data: ExpenseBase, db: Session = Depends(get_db), user: Users =Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == form_data.category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="category not found!")

    db_expense = Expenses(**form_data.model_dump(), user_id = user.id)

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return{
        "message" : "expense created",
        "data" : db_expense
    }