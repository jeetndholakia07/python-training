from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()