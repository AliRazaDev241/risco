"""API endpoints for Expenses"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import expenses as expense_service
from oracledb.exceptions import IntegrityError
from logger import get_logger
from datetime import datetime

logger = get_logger(__name__)

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# Add Expense
@router.post("/", response_model=schema.ExpenseResponse)
def add_expense(expense: schema.ExpenseCreate, db: Session = Depends(get_db)):
    try:
        return expense_service.add_expense(expense, db)
    except IntegrityError as e:
        raise HTTPException(status_code=404, detail="Organization not found")
    except Exception as e:
        logger.error("Failed to add expense: %s", e)
        raise HTTPException(status_code=500, detail="Failed to add expense")
