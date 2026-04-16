"""Setup for database connection that other modules use"""

from pathlib import Path
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Setup for logger
from logger import get_logger

logger = get_logger(__name__)

# Loads env file from Project Folder
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# Pull credentials from env file
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Get database url to use for connection
DATABASE_URL = (
    f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/?service_name={DB_NAME}"
)

# Connection to the database
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1 FROM DUAL"))
    logger.info("Database connection established successfully")
except Exception as e:
    logger.critical("Database connection failed: %s", e)

# Sessions created with the database for each request to use
SESSION_LOCAL = sessionmaker(bind=engine)

# Used in models to store classes to turn into database tables
Base = declarative_base()


def get_db():
    """FastAPI dependency function called when the database needs to be accessed"""
    db = SESSION_LOCAL()
    try:
        yield db
        logger.debug("Database session opened")
    except Exception as e:
        logger.error("Database session error: %s", e)
        db.rollback()
        raise
    finally:
        db.close()
        logger.debug("Database session closed")
