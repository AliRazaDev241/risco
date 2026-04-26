"""API endpoints for Members & Roles"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import organization_members as org_mem_service
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/organizations/{org_id}/members", tags=["Members & Roles"])


# get all members of an org
@router.get("/")
def list_members(org_id: int, db: Session = Depends(get_db)):
    return org_mem_service.get_all_members(org_id, db)


# add a member to an org
# add a member to an org
@router.post("/", status_code=201)
def add_member(
    org_id: int, data: schema.AddMemberRequest, db: Session = Depends(get_db)
):
    return org_mem_service.add_member(
        org_id, data.email, data.role_name, data.added_by, db
    )


# remove a member from an org
@router.delete("/{member_id}", status_code=200)
def remove_member(org_id: int, member_id: int, db: Session = Depends(get_db)):
    member = org_mem_service.get_member(member_id, org_id, db)
    if not member:
        raise HTTPException(
            status_code=404,
            detail=f"Member {member_id} not found in organization {org_id}",
        )
    return org_mem_service.remove_member(member_id, org_id, db)
