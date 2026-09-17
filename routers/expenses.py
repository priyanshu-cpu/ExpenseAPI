from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from models.expenses import Category, Expenses
from models.users import Users
from schemas.expenses import ExpenseOutSchema, ExpenseSchema
from routers.auth import verify_token, get_current_user


router = APIRouter(prefix="/expenses")


@router.post("/create", response_model=ExpenseOutSchema)
def create_expense(expense: ExpenseSchema, db: Session = Depends(get_db),current_user: Users = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == expense.category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_expense = Expenses(**expense.model_dump(), user_id = current_user.id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/get", response_model=list[ExpenseOutSchema])
def list_expenses(db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    return db.query(Expenses).filter(Expenses.user_id == current_user.id).all()


@router.get("/get/{expense_id}", response_model=ExpenseOutSchema)
def read_expense(expense_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    expense = db.query(Expenses).filter(Expenses.id == expense_id, Expenses.user_id == current_user.id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/update/{expense_id}", response_model=ExpenseOutSchema)
def update_expense(expense_id: int, expense: ExpenseSchema, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    db_expense = db.query(Expenses).filter(Expenses.id == expense_id, Expenses.user_id == current_user.id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    category = db.query(Category).filter(Category.id == expense.category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_expense.title = expense.title
    db_expense.price = expense.price
    db_expense.category_id = expense.category_id
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.delete("/delete/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db),current_user: Users = Depends(get_current_user)):
    expense = db.query(Expenses).filter(Expenses.id == expense_id, Expenses.user_id == current_user.id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted"}
