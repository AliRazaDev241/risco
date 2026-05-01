"""Business logic for Financial Snapshots"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, text
from models import Revenue, Expenses, Clients, FinancialSnapshots
from services import calculations as calculations_service
from logger import get_logger

logger = get_logger(__name__)

def get_range(org_id: int, start_date: datetime, end_date: datetime, db: Session):
    org = db.execute(text("SELECT id FROM organizations WHERE id = :org_id"), {"org_id": org_id}).fetchone()
    if not org:
        raise LookupError(f"No organization found with id {org_id}")
    return db.query(FinancialSnapshots).filter(
        FinancialSnapshots.organization_id == org_id,
        FinancialSnapshots.snapshot_date >= start_date,
        FinancialSnapshots.snapshot_date <= end_date
    ).order_by(FinancialSnapshots.snapshot_date.asc()).all()

def refresh_or_create(db: Session, org_id: int):
    _upsert_base(db, org_id)
    # _upsert_best(db, org_id)
    # _upsert_worst(db, org_id)

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
    projected = calculations_service.calculate_best(db, org_id)
    _upsert_snapshot(db, org_id, "best", projected.revenue, projected.expenses)
    pass


def _upsert_worst(db: Session, org_id: int):
    projected = calculations_service.calculate_worst(db, org_id)
    _upsert_snapshot(db, org_id, "worst", projected.revenue, projected.expenses)
    pass