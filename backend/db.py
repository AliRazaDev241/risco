from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pathlib import Path
import os

# Setup for logger
import logging
from logger import get_logger
logger = get_logger(__name__)

# Loads env file from Project Folder
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# Make and store database url using credentials for env file
DATABASE_URL = f"oracle+oracledb://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/?service_name={os.getenv('DB_NAME')}"

# Connection to the database
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1 FROM DUAL"))
    logger.info("Database connection established successfully")
except Exception as e:
    logger.critical(f"Database connection failed: {e}")
    raise

# Sessions created with the database for each request to use
SessionLocal = sessionmaker(bind=engine)

# Used in models to store classes to turn into database tables
Base = declarative_base()

# FastAPI dependency function that is called when the database needs to be accessed
def get_db():
    db = SessionLocal()
    try:
        yield db
        logger.debug("Database session opened")
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.debug("Database session closed")

