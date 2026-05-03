"""API endpoints for Expenses"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import expenses as expense_service
from coordinators import expense_coordinator
from logger import get_logger
from typing import Annotated, TypeAlias

logger = get_logger(__name__)
router = APIRouter(prefix="/expenses", tags=["Expenses"])
DbSession: TypeAlias = Annotated[Session, Depends(get_db)]


@router.post(
    "/",
    response_model=schema.ExpenseResponse,
    status_code=201,
    responses={
        404: {"description": "Organization not found"},
        500: {"description": "Failed to add expense"},
    },
)
def add_expense(expense: schema.ExpenseCreate, db: DbSession):
    try:
        return expense_coordinator.add_expense(expense, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logger.error("Failed to add expense")
        raise HTTPException(status_code=500, detail="Failed to add expense")


@router.get(
    "/",
    response_model=schema.ExpensePage,
    responses={
        404: {"description": "Organization not found"},
        500: {"description": "Failed to fetch expenses"},
    },
)
def list_expenses(org_id: int, expense_type: str, page_no: int, db: DbSession):
    try:
        return expense_service.list_five_expenses(org_id, expense_type, page_no, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logger.error("Failed to fetch expenses for org %s", org_id)
        raise HTTPException(status_code=500, detail="Failed to fetch expenses")
