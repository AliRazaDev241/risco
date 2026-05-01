"""Queries DB and assembles financial metrics"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, text
from models import Revenue, Clients
from services import calculations
from logger import get_logger

logger = get_logger(__name__)

def get_intelligence_metrics(org_id: int, db: Session) -> dict:
    now = datetime.now(timezone.utc)
    month, year = now.month, now.year

    org = db.execute(text("SELECT id FROM organizations WHERE id = :org_id"), {"org_id": org_id}).fetchone()
    if not org:
        raise LookupError(f"No organization found with id {org_id}")

    # all expected revenue this month with client reliability scores
    client_revenue = db.query(
        Revenue.amount,
        Clients.reliability_score
    ).join(
        Clients, Revenue.client_id == Clients.id
    ).filter(
        Clients.organization_id == org_id,
        extract('month', Revenue.date_expected) == month,
        extract('year', Revenue.date_expected) == year
    ).all()

    # actual received revenue this month
    actual_revenue = db.query(func.sum(Revenue.amount)).join(
        Clients, Revenue.client_id == Clients.id
    ).filter(
        Clients.organization_id == org_id,
        Revenue.date_received != None,
        extract('month', Revenue.date_received) == month,
        extract('year', Revenue.date_received) == year
    ).scalar() or 0

    amounts = [row.amount for row in client_revenue]
    scores = [row.reliability_score for row in client_revenue]

    return {
        "revenue_reliability_score": calculations.revenue_reliability_score(amounts, scores),
        "revenue_concentration_risk": calculations.revenue_concentration_risk(amounts),
        "reliable_revenue": calculations.reliable_revenue(amounts, scores),
        "total_revenue_expected": calculations.total_revenue(amounts),
        "actual_revenue": float(actual_revenue)
    }