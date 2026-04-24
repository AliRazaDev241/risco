""" Intiliazed db tables with roles"""
from db import SESSION_LOCAL
from models import Roles
from logger import get_logger

logger = get_logger(__name__)

def seed_roles():
    db = SESSION_LOCAL()

    try:
        logger.info("Starting role seeding...")

        # prevent duplicates
        existing = db.query(Roles).first()
        if existing:
            logger.info("Roles already exist — skipping seed")
            return

        roles = [
            Roles(role_name="owner", permission_level=1),
            Roles(role_name="coowner", permission_level=2),
            Roles(role_name="stakeholder", permission_level=3),
        ]

        db.add_all(roles)
        db.commit()

        logger.info("Roles seeded successfully")

    except Exception as e:
        db.rollback()
        logger.error("Role seeding failed: %s", e)

    finally:
        db.close()
        logger.debug("Database session closed")

if __name__ == "__main__":
    seed_roles()