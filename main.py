from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
def home():
    return{
        "message" : "DB Connection success"
    }
