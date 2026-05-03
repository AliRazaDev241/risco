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

@router.post("/graph", response_model=list[schema.GraphResponse])
def get_graph(snapshot: schema.GraphRequest, db: Session = Depends(get_db)):
    try:
        return snapshot_service.get_graph(snapshot, db)
    except LookupError as e:
        logger.error("Organization not found, id %s: %s", snapshot.org_id, e)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to fetch snapshots for org %s: %s", snapshot.org_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch snapshots")