"""Business logic for Financial Snapshots"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, text
from models import Revenue, Expenses, Clients, FinancialSnapshots
import schema
from services.calculations import revenue_concentration_risk, reliable_revenue
from logger import get_logger


logger = get_logger(__name__)

def get_graph(snapshot: schema.GraphRequest, db):
    org = db.execute(
        text("SELECT id FROM organizations WHERE id = :org_id"),
        {"org_id": snapshot.org_id}
    ).fetchone()
    if not org:
        raise LookupError(f"No organization found with id {snapshot.org_id}")

    rows = (
        db.query(FinancialSnapshots)
        .filter(
            FinancialSnapshots.organization_id == snapshot.org_id,
            FinancialSnapshots.snapshot_type == snapshot.snapshot_type,
            FinancialSnapshots.snapshot_date >= snapshot.start_date,
            FinancialSnapshots.snapshot_date <= snapshot.end_date,
        )
        .order_by(FinancialSnapshots.snapshot_date)
        .all()
    )

    return [
        {"snapshot_date": row.snapshot_date, "value": getattr(row, snapshot.metric_type)}
        for row in rows
    ]

def refresh_or_create(db: Session, org_id: int):
    _upsert_base(db, org_id)
    _upsert_best(db, org_id)
    _upsert_worst(db, org_id)

def _upsert_snapshot(db: Session, org_id: int, snapshot_type: str, monthly_revenue, monthly_expenses):
    now = datetime.now(timezone.utc)
    month, year = now.month, now.year
    cash_balance = monthly_revenue - monthly_expenses

    snapshot = db.query(FinancialSnapshots).filter(
        FinancialSnapshots.organization_id == org_id,
        extract('month', FinancialSnapshots.snapshot_date) == month,
        extract('year', FinancialSnapshots.snapshot_date) == year,
        FinancialSnapshots.snapshot_type == snapshot_type  # was .type
    ).first()

    if not snapshot:
        snapshot = FinancialSnapshots(
            organization_id=org_id,
            snapshot_date=now.date().replace(day=1),
            snapshot_type=snapshot_type,             # was type=
            monthly_revenue=monthly_revenue,
            monthly_expense=monthly_expenses,        # was monthly_expenses
            cash_balance=cash_balance
        )
        db.add(snapshot)
        logger.info("Created %s snapshot for org %s %s/%s", snapshot_type, org_id, month, year)
    else:
        snapshot.monthly_revenue = monthly_revenue
        snapshot.monthly_expense = monthly_expenses  # was monthly_expenses
        snapshot.cash_balance = cash_balance
        logger.info("Updated %s snapshot for org %s %s/%s", snapshot_type, org_id, month, year)

    db.commit()

def _upsert_base(db: Session, org_id: int):
    now = datetime.now(timezone.utc)
    month, year = now.month, now.year

    monthly_expenses = db.query(func.sum(Expenses.amount)).filter(
        Expenses.organization_id == org_id,
        extract('month', Expenses.date) == month,
        extract('year', Expenses.date) == year
    ).scalar() or 0

    monthly_revenue = db.query(func.sum(Revenue.amount)).join(
        Clients, Revenue.client_id == Clients.id
    ).filter(
        Clients.organization_id == org_id,
        extract('month', Revenue.date_received) == month,
        extract('year', Revenue.date_received) == year
    ).scalar() or 0

    _upsert_snapshot(db, org_id, "Base", monthly_revenue, monthly_expenses)  # capital B to match constraint

def _upsert_best(db: Session, org_id: int):
    now = datetime.now(timezone.utc)
    month, year = now.month, now.year

    expected_amounts = db.execute(text("""
        SELECT r.amount FROM revenue r
        JOIN clients c ON c.id = r.client_id
        WHERE c.organization_id = :org_id
        AND EXTRACT(MONTH FROM r.date_expected) = :month
        AND EXTRACT(YEAR FROM r.date_expected) = :year
    """), {"org_id": org_id, "month": month, "year": year}).fetchall()

    non_critical_expenses = db.execute(text("""
        SELECT NVL(SUM(amount), 0) FROM expenses
        WHERE organization_id = :org_id
        AND urgency = 'Non-Critical'
        AND EXTRACT(MONTH FROM "date") = :month
        AND EXTRACT(YEAR FROM "date") = :year
    """), {"org_id": org_id, "month": month, "year": year}).scalar()

    amounts = [row.amount for row in expected_amounts]
    _upsert_snapshot(db, org_id, "Best", sum(amounts), non_critical_expenses)

def _upsert_worst(db: Session, org_id: int):
    now = datetime.now(timezone.utc)
    month, year = now.month, now.year

    client_revenue = db.execute(text("""
        SELECT r.amount, c.reliability_score FROM revenue r
        JOIN clients c ON c.id = r.client_id
        WHERE c.organization_id = :org_id
        AND EXTRACT(MONTH FROM r.date_expected) = :month
        AND EXTRACT(YEAR FROM r.date_expected) = :year
    """), {"org_id": org_id, "month": month, "year": year}).fetchall()

    all_expenses = db.execute(text("""
        SELECT NVL(SUM(amount), 0) FROM expenses
        WHERE organization_id = :org_id
        AND EXTRACT(MONTH FROM "date") = :month
        AND EXTRACT(YEAR FROM "date") = :year
    """), {"org_id": org_id, "month": month, "year": year}).scalar()

    amounts = [row.amount for row in client_revenue]
    # scores = [row.reliability_score for row in client_revenue]
    scores = [row.reliability_score if row.reliability_score is not None else 0 for row in client_revenue]
    _upsert_snapshot(db, org_id, "Worst", reliable_revenue(amounts, scores), all_expenses)