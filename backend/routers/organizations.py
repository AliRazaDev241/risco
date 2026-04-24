""" API endpoints for Organizations """
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import organizations as org_service
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/organizations", tags=["Organizations"])

# check if user has an org after login
@router.get("/user/{user_id}", response_model=schema.OrganizationResponse)
def get_user_organization(user_id: int, db: Session = Depends(get_db)):
    member = org_service.check_membership_by_user(user_id, db)
    if not member:
        raise HTTPException(status_code=404, detail="No organization found")
    org = org_service.get_organization_by_id(member.organization_id, db)
    return org

# create an org
@router.post("/", response_model=schema.OrganizationResponse)
def create_organization(
    org: schema.OrganizationCreate,
    creator_id: int,
    role_id: int,
    db: Session = Depends(get_db)
):
    existing = org_service.get_organization_by_name(org.org_name, db)
    if existing:
        raise HTTPException(status_code=400, detail="Organization name already taken")
    return org_service.create_organization(org, creator_id, role_id, db)

# join an org
@router.post("/join", response_model=schema.OrganizationResponse)
def join_organization(
    request: schema.OrganizationJoinRequest,
    db: Session = Depends(get_db)
):
    org = org_service.get_organization_by_name(request.org_name, db)
    if not org:
        raise HTTPException(status_code=404, detail="Organization does not exist")
    membership = org_service.check_membership(request.user_id, org.id, db)
    if not membership:
        raise HTTPException(status_code=403, detail="You have not been added to this organization, contact your admin")
    return org