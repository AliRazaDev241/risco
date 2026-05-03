"""Orchestrates expense writes and snapshot refresh"""

from sqlalchemy.orm import Session
from services import expenses as expense_service
from services import snapshots as snapshot_service


def add_expense(expense, db: Session):
    result = expense_service.add_expense(expense, db)
    snapshot_service.refresh_or_create(db, result.organization_id)
    return result
