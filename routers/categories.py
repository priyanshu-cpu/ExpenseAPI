from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from models.expenses import Category, Expenses
from schemas.expenses import CategoryOutSchema, CategorySChema

router = APIRouter(prefix="/categories")

@router.post("/categories", response_model=CategoryOutSchema)
def create_category(category: CategorySChema, db : Session = Depends(get_db)):
    category_dict = category.model_dump()
    db_category = Category(**category_dict)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/categories", response_model=list[CategoryOutSchema])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.get("/categories/{category_id}", response_model=CategoryOutSchema)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/categories/{category_id}", response_model=CategoryOutSchema)
def update_category(category_id: int, category: CategorySChema, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}

