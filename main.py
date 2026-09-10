from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base, get_db
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
