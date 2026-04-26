"""API endpoints for Members & Roles"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import clients as client_service
from logger import get_logger

logger = get_logger(__name__)


router = APIRouter(prefix="/organizations/{org_id}/members", tags=["Members & Roles"])

# Add Expense
@router.post("/", response_model=schema.ClientsResponse)
def add_client(expense: schema.ExpenseCreate, db: Session = Depends(get_db)):
    try:
        return expense_service.add_expense(expense, db)
    except IntegrityError as e:
        raise HTTPException(status_code=404, detail="Organization not found")
    except Exception as e:
        logger.error("Failed to add expense: %s", e)
        raise HTTPException(status_code=500, detail="Failed to add expense")
