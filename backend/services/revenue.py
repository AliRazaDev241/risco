"""Business logic for Revenue"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Revenue
import schema
from logger import get_logger
logger = get_logger(__name__)

def add_revenue(revenue: schema.RevenueCreate, db: Session):
    client_row = db.execute(
        text("SELECT id FROM clients WHERE name = :name"),
        {"name": revenue.client_name}
    ).fetchone()
    if not client_row:
        raise LookupError(f"No client found with name {revenue.client_name}")

    try:
        new_revenue = Revenue(
            client_id=client_row.id,
            revenue_type=revenue.revenue_type,
            date_expected=revenue.date_expected,
            date_received=revenue.date_received,
            amount=revenue.amount,
        )
        db.add(new_revenue)
        db.commit()
        db.refresh(new_revenue)
        logger.info("Revenue added for client %s", revenue.client_name)
        return new_revenue
    except Exception as e:
        db.rollback()
        raise