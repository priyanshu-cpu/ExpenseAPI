from app.models.expenses import Category, Expenses
from app.models.users import Users
from app.schemas.expenses import CategoryBase, CategoryOut, CategoryCreateResponse
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import get_current_user, verify_token


router = APIRouter(prefix="/category")



@router.get("/get", response_model=list[CategoryOut])
def list_categories(db:Session = Depends(get_db), user: Users = Depends(get_current_user)):
    categories =  db.query(Category).filter(Category.user_id == user.id).all()
    if not categories:
        raise HTTPException(status_code=404, detail="no category found!")
    return categories



@router.get("/get/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db:Session = Depends(get_db), user:Users = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    return category



@router.post("/create", response_model=CategoryCreateResponse)
def create_category(form_data : CategoryBase, db:Session = Depends(get_db),user:Users = Depends(get_current_user)):
    category = db.query(Category).filter(Category.name == form_data.name, Category.user_id == user.id).first()
    if category:
        raise HTTPException(status_code=400, detail="category already exists")
    new_category = Category(name = form_data.name, user_id = user.id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return{
        "message" : "category created",
        "data" : new_category
    }



@router.put("/update/{category_id}", response_model=CategoryCreateResponse)
def update_category(category_id: int, form_data: CategoryBase, db: Session = Depends(get_db), user:Users = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == user.id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="category not found!")

    category.name = form_data.name
    db.commit()
    db.refresh(category)
    return {
        "message" : "category updated",
        "data" : category
    }



@router.delete("/delete/{category_id}")
def delete_category(category_id : int, db: Session = Depends(get_db), user:Users = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == user.id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Not found!")
    db.delete(category)
    db.commit()
    return{
        "message" : "category deleted"
    }