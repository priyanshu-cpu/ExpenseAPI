from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.settings import settings


engine = create_engine(settings.DB_CONNECTION)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        