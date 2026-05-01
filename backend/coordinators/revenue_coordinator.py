"""Orchestrates revenue writes and snapshot refresh"""
from sqlalchemy.orm import Session
from models import Clients
from services import revenue as revenue_service
from services import snapshots as snapshot_service
from logger import get_logger

logger = get_logger(__name__)

def add_revenue(revenue, db: Session):
    result = revenue_service.add_revenue(revenue, db)
    snapshot_service.refresh_or_create(db, revenue.org_id)  # use request directly, no extra query
    return result

def update_revenue(revenue_id, revenue, db: Session):
    result = revenue_service.update_revenue(revenue_id, revenue, db)
    client = db.query(Clients).filter(Clients.id == result.client_id).first()  # still needed, no org_id in update body
    snapshot_service.refresh_or_create(db, client.organization_id)
    return result