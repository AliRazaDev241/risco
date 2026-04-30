"""Business logic for Expenses"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Expenses
import schema
from logger import get_logger
logger = get_logger(__name__)

def add_expense(expense: schema.ExpenseCreate, db: Session):
    org = db.execute(
        text("SELECT id FROM organizations WHERE id = :org_id"),
        {"org_id": expense.organization_id}
    ).fetchone()
    if not org:
        raise LookupError(f"No organization found with id {expense.organization_id}")
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
        logger.info("Expense added for org %s", expense.organization_id)
        return new_expense
    except Exception as e:
        db.rollback()
        raise


def list_five_expenses(org_id: int, expense_type: str, page_no: int, db: Session):
    org = db.execute(
        text("SELECT id FROM organizations WHERE id = :org_id"),
        {"org_id": org_id}
    ).fetchone()
    if not org:
        raise LookupError(f"No organization found with id {org_id}")

    params = {"org_id": org_id, "expense_type": expense_type}

    count = db.execute(text("""
        SELECT COUNT(*) FROM expenses
        WHERE organization_id = :org_id
        AND expense_type = :expense_type
    """), params).scalar()

    total_pages = max(1, -(-count // 5))
    offset = (page_no - 1) * 5

    rows = db.execute(text("""
        SELECT urgency, expense_type, "date", amount
        FROM expenses
        WHERE organization_id = :org_id
        AND expense_type = :expense_type
        ORDER BY "date" ASC, id ASC
        OFFSET :offset ROWS FETCH NEXT 5 ROWS ONLY
    """), {**params, "offset": offset}).fetchall()
    
    return {"items": rows, "total_pages": total_pages, "current_page": page_no}