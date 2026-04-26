""" API endpoints for Members & Roles """
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import mem_role as mem_role_service
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/organizations/{org_id}/members", tags=["Members & Roles"])

# get all members of an org
@router.get("/")
def list_members(org_id: int, db: Session = Depends(get_db)):
    return mem_role_service.get_all_members(org_id, db)

# add a member to an org
@router.post("/", status_code=201)
def add_member(org_id: int, data: schema.AddMemberRequest, db: Session = Depends(get_db)):
    existing = mem_role_service.get_member(data.member_id, org_id, db)
    if existing:
        raise HTTPException(status_code=409, detail=f"User {data.member_id} is already a member of this organization")
    return mem_role_service.add_member(org_id, data.member_id, data.role_id, data.added_by, db)

# remove a member from an org
@router.delete("/{member_id}", status_code=200)
def remove_member(org_id: int, member_id: int, db: Session = Depends(get_db)):
    member = mem_role_service.get_member(member_id, org_id, db)
    if not member:
        raise HTTPException(status_code=404, detail=f"Member {member_id} not found in organization {org_id}")
    return mem_role_service.remove_member(member_id, org_id, db)