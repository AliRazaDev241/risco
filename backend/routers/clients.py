"""API endpoints for Clients"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import clients as client_service
from oracledb.exceptions import IntegrityError
from logger import get_logger
logger = get_logger(__name__)

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=schema.ClientsResponse, status_code=201)
def add_client(client: schema.ClientsCreate, db: Session = Depends(get_db)):
    try:
        return client_service.add_client(client, db)
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Organization not found")
    except Exception as e:
        logger.error("Failed to add client: %s", e)
        raise HTTPException(status_code=500, detail="Failed to add client")