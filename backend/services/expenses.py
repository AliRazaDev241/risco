"""Business logic for Expenses"""

from sqlalchemy.orm import Session
from models import Expenses
import schema
from logger import get_logger

logger = get_logger(__name__)


def add_expense(expense: schema.ExpenseCreate, db: Session):
    try:
        new_expense = Expenses(
            organization_id=expense.organization_id,
            urgency=expense.urgency,
            expense_type=expense.expense_type,
            date=expense.date,
            amount=expense.amount,
        )
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
        logger.info("Expense added for org_id: %s", new_expense.organization_id)
        return new_expense
    except Exception as e:
        db.rollback()
        raise
