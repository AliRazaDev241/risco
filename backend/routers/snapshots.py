"""API endpoints for Financial Snapshots"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import snapshots as snapshot_service
from logger import get_logger
from datetime import datetime

logger = get_logger(__name__)
router = APIRouter(prefix="/snapshots", tags=["Snapshots"])

@router.get("/", response_model=list[schema.SnapshotResponse])
def get_snapshots(org_id: int, start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    try:
        return snapshot_service.get_range(org_id, start_date, end_date, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to fetch snapshots for org %s: %s", org_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch snapshots")