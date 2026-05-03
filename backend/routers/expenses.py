"""API endpoints for Expenses"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import expenses as expense_service
from coordinators import expense_coordinator
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=schema.ExpenseResponse, status_code=201)
def add_expense(expense: schema.ExpenseCreate, db: Session = Depends(get_db)):
    try:
        return expense_coordinator.add_expense(expense, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to add expense: %s", e)
        raise HTTPException(status_code=500, detail="Failed to add expense")


@router.get("/", response_model=schema.ExpensePage)
def list_expenses(
    org_id: int, expense_type: str, page_no: int, db: Session = Depends(get_db)
):
    try:
        return expense_service.list_five_expenses(org_id, expense_type, page_no, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to fetch expenses for org %s: %s", org_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch expenses")
