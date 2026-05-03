"""API endpoints for Revenue"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import revenue as revenue_service
from coordinators import revenue_coordinator
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/revenue", tags=["Revenue"])


@router.post("/", response_model=schema.RevenueResponse, status_code=201)
def add_revenue(revenue: schema.RevenueCreate, db: Session = Depends(get_db)):
    try:
        return revenue_coordinator.add_revenue(revenue, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        if "CHK_REVENUE_AMOUNT" in str(e):
            raise HTTPException(status_code=422, detail="Amount must be greater than 0")
        logger.error("Failed to add revenue: %s", e)
        raise HTTPException(status_code=500, detail="Failed to add revenue")


@router.get("/", response_model=schema.RevenuePage)
def list_revenue(
    org_id: int, revenue_type: str, page_no: int, db: Session = Depends(get_db)
):
    try:
        return revenue_service.list_five_revenue(org_id, revenue_type, page_no, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to fetch revenue for org %s: %s", org_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch revenue")


@router.patch("/{revenue_id}", response_model=schema.RevenueResponse)
def update_revenue(
    revenue_id: int, revenue: schema.RevenueUpdate, db: Session = Depends(get_db)
):
    try:
        updated = revenue_coordinator.update_revenue(revenue_id, revenue, db)
        logger.info("Revenue %s updated successfully", revenue_id)
        return updated
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to update revenue %s: %s", revenue_id, e)
        raise HTTPException(status_code=500, detail="Failed to update revenue")
