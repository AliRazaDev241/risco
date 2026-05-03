"""API endpoints for Financial Snapshots"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import snapshots as snapshot_service
from logger import get_logger
from typing import Annotated, TypeAlias

logger = get_logger(__name__)
router = APIRouter(prefix="/snapshots", tags=["Snapshots"])
DbSession: TypeAlias = Annotated[Session, Depends(get_db)]


@router.post(
    "/graph",
    response_model=schema.GraphResponse,
    responses={
        404: {"description": "Organization not found"},
        500: {"description": "Failed to fetch Graph Data"},
    },
)
def get_graph(snapshot: schema.GraphRequest, db: DbSession):
    try:
        return snapshot_service.get_graph(snapshot, db)
    except LookupError as e:
        logger.error("Organization not found, id %s: %s", snapshot.org_id, e)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logger.error("Failed to fetch snapshots for org %s", snapshot.org_id)
        raise HTTPException(status_code=500, detail="Failed to fetch Graph Data")
