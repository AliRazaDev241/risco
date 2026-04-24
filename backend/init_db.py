from db import engine, Base
from models import *  # make sure all models are imported
from logger import get_logger

logger = get_logger(__name__)

def reset_db():
    logger.info("Dropping all tables...")

    Base.metadata.drop_all(bind=engine)

    logger.info("Creating all tables...")

    Base.metadata.create_all(bind=engine)

    logger.info("Database reinitialized successfully")

if __name__ == "__main__":
    reset_db()