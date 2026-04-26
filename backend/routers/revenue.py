"""API endpoints for Revenue"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import revenue as revenue_service
from logger import get_logger
logger = get_logger(__name__)
router = APIRouter(prefix="/revenue", tags=["Revenue"])

@router.post("/", response_model=schema.RevenueResponse, status_code=201)
def add_revenue(revenue: schema.RevenueCreate, db: Session = Depends(get_db)):
    try:
        return revenue_service.add_revenue(revenue, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to add revenue: %s", e)
        raise HTTPException(status_code=500, detail="Failed to add revenue")