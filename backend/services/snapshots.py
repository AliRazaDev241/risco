"""Business logic for Financial Snapshots"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from models import Revenue, Expenses, Clients, FinancialSnapshots
from logger import get_logger

logger = get_logger(__name__)
"""Business logic for Financial Snapshots"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from models import Revenue, Expenses, Clients, FinancialSnapshots
from logger import get_logger

logger = get_logger(__name__)


def refresh_or_create(db: Session, org_id: int):
    """Called after every revenue/expense write. Updates all snapshot types."""
    _upsert_base(db, org_id)
    # _upsert_best(db, org_id)
    # _upsert_worst(db, org_id)


def _upsert_base(db: Session, org_id: int):
    """ Private function that inserts or updates base snapshot """
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

    cash_balance = monthly_revenue - monthly_expenses

    snapshot = db.query(FinancialSnapshots).filter(
        FinancialSnapshots.organization_id == org_id,
        extract('month', FinancialSnapshots.snapshot_date) == month,
        extract('year', FinancialSnapshots.snapshot_date) == year,
        FinancialSnapshots.type == "base"
    ).first()

    if not snapshot:
        snapshot = FinancialSnapshots(
            organization_id=org_id,
            snapshot_date=now.date().replace(day=1),
            type="base",
            monthly_revenue=monthly_revenue,
            monthly_expenses=monthly_expenses,
            cash_balance=cash_balance
        )
        db.add(snapshot)
        logger.info("Created base snapshot for org %s %s/%s", org_id, month, year)
    else:
        snapshot.monthly_revenue = monthly_revenue
        snapshot.monthly_expenses = monthly_expenses
        snapshot.cash_balance = cash_balance
        logger.info("Updated base snapshot for org %s %s/%s", org_id, month, year)

    db.commit()


def _upsert_best(db: Session, org_id: int):
    """ Private function that inserts or updates best snapshot """
    # TODO: implement when predictive module is ready
    # Uses client reliability scores and NumPy projections
    pass


def _upsert_worst(db: Session, org_id: int):
    """ Private function that inserts or updates worst snapshot """
    # TODO: implement when predictive module is ready
    # Uses client reliability scores and NumPy projections
    pass