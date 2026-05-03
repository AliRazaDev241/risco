"""Queries DB and assembles financial metrics"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import text
from services import calculations
from logger import get_logger

logger = get_logger(__name__)

def get_intelligence_metrics(org_id: int, db: Session):
    now = datetime.now(timezone.utc)
    month, year = now.month, now.year

    org = db.execute(text("SELECT id FROM organizations WHERE id = :org_id"), {"org_id": org_id}).fetchone()
    if not org:
        raise LookupError(f"No organization found with id {org_id}")

    # All expected revenue this month with client reliability scores
    client_revenue = db.execute(text("""
        SELECT r.amount, c.reliability_score
        FROM revenue r
        JOIN clients c ON c.id = r.client_id
        WHERE c.organization_id = :org_id
        AND EXTRACT(MONTH FROM r.date_expected) = :month
        AND EXTRACT(YEAR FROM r.date_expected) = :year
    """), {"org_id": org_id, "month": month, "year": year}).fetchall()

    # Actual received revenue this month
    actual_revenue = db.execute(text("""
        SELECT NVL(SUM(r.amount), 0)
        FROM revenue r
        JOIN clients c ON c.id = r.client_id
        WHERE c.organization_id = :org_id
        AND r.date_received IS NOT NULL
        AND EXTRACT(MONTH FROM r.date_received) = :month
        AND EXTRACT(YEAR FROM r.date_received) = :year
    """), {"org_id": org_id, "month": month, "year": year}).scalar()

    amounts = [row.amount for row in client_revenue]
    scores = [row.reliability_score if row.reliability_score is not None else 0 for row in client_revenue]

    return {
        "revenue_reliability_score": calculations.revenue_reliability_score(amounts, scores),
        "revenue_concentration_risk": calculations.revenue_concentration_risk(amounts),
        "reliable_revenue": calculations.reliable_revenue(amounts, scores),
        "total_revenue_expected": calculations.total_revenue(amounts),
        "actual_revenue": float(actual_revenue)
    }


def get_dashboard_metrics(org_id: int, db: Session):
    now = datetime.now(timezone.utc)
    month, year = now.month, now.year

    org = db.execute(text("SELECT id FROM organizations WHERE id = :org_id"), {"org_id": org_id}).fetchone()
    if not org:
        raise LookupError(f"No organization found with id {org_id}")

    # Revenue received this month
    monthly_revenue = db.execute(text("""
        SELECT NVL(SUM(r.amount), 0)
        FROM revenue r
        JOIN clients c ON c.id = r.client_id
        WHERE c.organization_id = :org_id
        AND r.date_received IS NOT NULL
        AND EXTRACT(MONTH FROM r.date_received) = :month
        AND EXTRACT(YEAR FROM r.date_received) = :year
    """), {"org_id": org_id, "month": month, "year": year}).scalar()

    # All expenses this month
    monthly_expenses = db.execute(text("""
        SELECT NVL(SUM(amount), 0)
        FROM expenses
        WHERE organization_id = :org_id
        AND EXTRACT(MONTH FROM "date") = :month
        AND EXTRACT(YEAR FROM "date") = :year
    """), {"org_id": org_id, "month": month, "year": year}).scalar()

    # Previous cash balance from the most recent snapshot
    prev_balance = db.execute(text("""
        SELECT cash_balance
        FROM financial_snapshots
        WHERE organization_id = :org_id
        ORDER BY snapshot_date DESC
        FETCH FIRST 1 ROWS ONLY
    """), {"org_id": org_id}).scalar()

    # Headcount
    headcount = db.execute(text("""
        SELECT COUNT(member_id)
        FROM organization_members
        WHERE organization_id = :org_id
    """), {"org_id": org_id}).scalar() or 0

    current_balance = calculations.cash_balance(prev_balance, float(monthly_revenue), float(monthly_expenses))

    return {
        "cash_runway": calculations.cash_runway(current_balance, float(monthly_expenses)),
        "burn_rate": monthly_expenses,
        "cash_balance": int(current_balance),
        "monthly_revenue": int(monthly_revenue),
        "headcount": headcount,
    }