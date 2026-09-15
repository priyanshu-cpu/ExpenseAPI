from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from models.expenses import Category, Expenses
import schemas


router = APIRouter(prefix="/expenses")



@router.post("/expenses", response_model=schemas.ExpenseOut)
def create_expense(expense: schemas.Expense, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == expense.category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_expense = Expenses(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/expenses", response_model=list[schemas.ExpenseOut])
def list_expenses(db: Session = Depends(get_db)):
    return db.query(Expenses).all()


@router.get("/expenses/{expense_id}", response_model=schemas.ExpenseOut)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expenses).filter(Expenses.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/expenses/{expense_id}", response_model=schemas.ExpenseOut)
def update_expense(expense_id: int, expense: schemas.Expense, db: Session = Depends(get_db)):
    db_expense = db.query(Expenses).filter(Expenses.id == expense_id).first()
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


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expenses).filter(Expenses.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted"}
