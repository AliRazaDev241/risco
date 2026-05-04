""" Refreshes and Reinitialized the database """
from db import engine, Base
import models
from logger import get_logger

logger = get_logger(__name__)


def reset_db():
    """ Resets the db tables using models.py """
    logger.info("Dropping all tables...")

    Base.metadata.drop_all(bind=engine)

    logger.info("Creating all tables...")

    Base.metadata.create_all(bind=engine)

    logger.info("Database reinitialized successfully")


if __name__ == "__main__":
    reset_db()
