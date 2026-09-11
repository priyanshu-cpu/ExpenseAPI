from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import schemas

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
def home():
    return{
        "message" : "Home Page"
    }

@app.post("/categories", response_model=schemas.CategoryOut)
def create_category(category: schemas.Category, db : Session = Depends(get_db)):
    category_dict = category.model_dump()
    db_category = models.Category(**category_dict)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/categories", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


@app.get("/categories/{category_id}", response_model=schemas.CategoryOut)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.put("/categories/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: int, category: schemas.Category, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}


@app.post("/expenses", response_model=schemas.ExpenseOut)
def create_expense(expense: schemas.Expense, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == expense.category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_expense = models.Expenses(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/expenses", response_model=list[schemas.ExpenseOut])
def list_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expenses).all()


@app.get("/expenses/{expense_id}", response_model=schemas.ExpenseOut)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expenses).filter(models.Expenses.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.put("/expenses/{expense_id}", response_model=schemas.ExpenseOut)
def update_expense(expense_id: int, expense: schemas.Expense, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expenses).filter(models.Expenses.id == expense_id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    category = db.query(models.Category).filter(models.Category.id == expense.category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db_expense.title = expense.title
    db_expense.price = expense.price
    db_expense.category_id = expense.category_id
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expenses).filter(models.Expenses.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted"}
