"""API endpoints for financial intelligence and dashboard metrics"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import financial as financial_service
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/financial", tags=["Financial"])

@router.get("/intelligence", response_model=schema.IntelligenceResponse)
def get_intelligence(org_id: int, db: Session = Depends(get_db)):
    try:
        return financial_service.get_intelligence_metrics(org_id, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to fetch intelligence metrics for org %s: %s", org_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch intelligence metrics")
    
@router.get("/dashboard", response_model=schema.DashboardResponse)
def get_dashboard(org_id: int, db: Session = Depends(get_db)):
    try:
        return financial_service.get_dashboard_metrics(org_id, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to fetch intelligence metrics for org %s: %s", org_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch Dashboard Metrics")