"""API endpoints for Clients"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db import get_db
import schema
from services import clients as client_service
from logger import get_logger
from typing import Annotated, TypeAlias

logger = get_logger(__name__)
router = APIRouter(prefix="/clients", tags=["Clients"])
DbSession: TypeAlias = Annotated[Session, Depends(get_db)]

@router.post(
    "/",
    response_model=schema.ClientsResponse,
    status_code=201,
    responses={
        404: {"description": "Organization not found"},
        409: {"description": "Client with this email or contact number already exists"},
        500: {"description": "Failed to add client"},
    }
)
def add_client(client: schema.ClientsCreate, db: DbSession):
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
    except Exception:
        logger.error("Failed to add client")
        raise HTTPException(status_code=500, detail="Failed to add client")