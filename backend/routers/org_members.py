""" API endpoints for Organization Members """
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import org_members as mem_services
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/members", tags=["members"])

@router.post("/", response_model = schema.OrgMemberResponse)
def add_member(member: schema.OrgMemberCreate, db: Session = Depends(get_db)):
    existing = mem_services.get_user_by_id(member.member_id, db)