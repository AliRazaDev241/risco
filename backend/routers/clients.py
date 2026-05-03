"""API endpoints for Clients"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from db import get_db
import schema
from services import clients as client_service
from logger import get_logger
logger = get_logger(__name__)

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=schema.ClientsResponse, status_code=201)
def add_client(client: schema.ClientsCreate, db: Session = Depends(get_db)):
    try:
        return client_service.add_client(client, db)
    except IntegrityError as e:
        err = str(e.orig)
        if "SYS_C008330" in err:
            raise HTTPException(status_code=409, detail="Client with this email already exists")
        elif "SYS_C008331" in err:
            raise HTTPException(status_code=409, detail="Client with this contact number already exists")
        elif "SYS_C008332" in err:
            raise HTTPException(status_code=404, detail="Organization not found")
        else:
            raise HTTPException(status_code=409, detail="Database constraint violated")
    except Exception as e:
        logger.error("Failed to add client: %s", e)
        raise HTTPException(status_code=500, detail="Failed to add client")
    

def update_reliability_score(db: Session, client_id: int):
    score = recalculate_reliability(db, client_id)
    db.execute(text("""
        UPDATE clients SET reliability_score = :score
        WHERE id = :client_id
    """), {"score": score, "client_id": client_id})
    db.commit()


MAX_DAYS_LATE = 90

def recalculate_reliability(db: Session, client_id: int) -> int:
    rows = db.execute(text("""
        SELECT GREATEST(0, CAST(date_received - date_expected AS NUMBER)) AS days_late
        FROM revenue
        WHERE client_id = :client_id
        AND date_received IS NOT NULL
    """), {"client_id": client_id}).fetchall()

    if not rows:
        return 100  # no payment history, benefit of the doubt

    contributions = [max(0.0, 1 - (row.days_late / MAX_DAYS_LATE)) for row in rows]
    score = round(sum(contributions) / len(contributions) * 100)
    return min(score, 100)