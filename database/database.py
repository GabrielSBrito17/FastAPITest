import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('NAME_DB')
db_password = os.getenv('PASSWORD_DB')
db_server = os.getenv('SERVER')
db_name = os.getenv('DB')

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_server}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()