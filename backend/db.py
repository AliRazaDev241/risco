from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pathlib import Path
import os
import logs

# Loads env file from Project Folder
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# Make and store database url using credentials for env file
DATABASE_URL = f"oracle+oracledb://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/?service_name={os.getenv('DB_NAME')}"

# Connection to the database
engine = create_engine(DATABASE_URL)
# Sessions created with the database for each request to use
SessionLocal = sessionmaker(bind=engine)

# Used in models to store classes to turn into database tables
Base = declarative_base()

# FastAPI dependency function that is called when the database needs to be accessed
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# remove comments to test connection with database
"""
try:
    with engine.connect() as conn:
        print("Connected to Oracle successfully!")
except Exception as e:
    print(f"Connection failed: {e}")
"""