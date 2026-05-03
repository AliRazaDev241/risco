"""API endpoints for financial intelligence and dashboard metrics"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import financial as financial_service
from logger import get_logger
from typing import Annotated, TypeAlias

logger = get_logger(__name__)
router = APIRouter(prefix="/financial", tags=["Financial"])
DbSession: TypeAlias = Annotated[Session, Depends(get_db)]


@router.get(
    "/intelligence",
    response_model=schema.IntelligenceResponse,
    responses={
        404: {"description": "Organization not found"},
        500: {"description": "Failed to fetch intelligence metrics"},
    },
)
def get_intelligence(org_id: int, db: DbSession):
    try:
        return financial_service.get_intelligence_metrics(org_id, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logger.error("Failed to fetch intelligence metrics for org %s", org_id)
        raise HTTPException(
            status_code=500, detail="Failed to fetch intelligence metrics"
        )


@router.get(
    "/dashboard",
    response_model=schema.DashboardResponse,
    responses={
        404: {"description": "Organization not found"},
        500: {"description": "Failed to fetch Dashboard Metrics"},
    },
)
def get_dashboard(org_id: int, db: DbSession):
    try:
        return financial_service.get_dashboard_metrics(org_id, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logger.error("Failed to fetch dashboard metrics for org %s", org_id)
        raise HTTPException(status_code=500, detail="Failed to fetch Dashboard Metrics")
