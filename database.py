from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base =  declarative_base()

DB_CONNECTION = "<db conn string>"

engine = create_engine()

LocalSession = sessionmaker(bind=engine)