"""API endpoints for Organizations"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import organizations as org_service
from logger import get_logger
from typing import Annotated, TypeAlias

logger = get_logger(__name__)
router = APIRouter(prefix="/organizations", tags=["Organizations"])
DbSession: TypeAlias = Annotated[Session, Depends(get_db)]


@router.get(
    "/user/{user_id}",
    response_model=schema.OrganizationResponse,
    responses={404: {"description": "No organization found"}},
)
def get_user_organization(user_id: int, db: DbSession):
    member = org_service.check_membership_by_user(user_id, db)
    if not member:
        raise HTTPException(status_code=404, detail="No organization found")
    return org_service.get_organization_by_id(member.organization_id, db)


@router.post(
    "/",
    response_model=schema.OrganizationResponse,
    responses={400: {"description": "Organization name already taken"}},
)
def create_organization(org: schema.OrganizationCreate, creator_id: int, db: DbSession):
    existing = org_service.get_organization_by_name(org.org_name, db)
    if existing:
        raise HTTPException(status_code=400, detail="Organization name already taken")
    return org_service.create_organization(org, creator_id, db)


@router.post(
    "/join",
    response_model=schema.OrganizationResponse,
    responses={
        404: {"description": "Organization does not exist"},
        403: {"description": "User has not been added to this organization"},
    },
)
def join_organization(request: schema.OrganizationJoinRequest, db: DbSession):
    org = org_service.get_organization_by_name(request.org_name, db)
    if not org:
        raise HTTPException(status_code=404, detail="Organization does not exist")
    membership = org_service.check_membership(request.user_id, org.id, db)
    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You have not been added to this organization, contact your admin",
        )
    return org
