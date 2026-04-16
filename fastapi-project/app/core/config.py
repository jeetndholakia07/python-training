from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()