from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

Base =  declarative_base()
load_dotenv()
DB_URL = os.getenv("DB_CONNECTION")

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
