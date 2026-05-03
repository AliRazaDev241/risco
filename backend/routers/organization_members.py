"""API endpoints for Members & Roles"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import organization_members as org_mem_service
from logger import get_logger
from typing import Annotated, TypeAlias

logger = get_logger(__name__)
DbSession: TypeAlias = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/organizations/{org_id}/members", tags=["Members & Roles"])

@router.get(
    "/",
    response_model=list[schema.MemberListResponse],
    responses={500: {"description": "Failed to fetch members"}}
)
def list_members(org_id: int, db: DbSession):
    try:
        return org_mem_service.get_all_members(org_id, db)
    except Exception:
        logger.error("Failed to fetch members for org %s", org_id)
        raise HTTPException(status_code=500, detail="Failed to fetch members")

@router.post(
    "/",
    status_code=201,
    responses={
        404: {"description": "User not found"},
        409: {"description": "Member is already part of the organization"},
        500: {"description": "Failed to add member"},
    }
)
def add_member(org_id: int, data: schema.AddMemberRequest, db: DbSession):
    try:
        return org_mem_service.add_member(org_id, data.email, data.role_name, data.added_by, db)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception:
        logger.error("Failed to add member to org %s", org_id)
        raise HTTPException(status_code=500, detail="Failed to add member")

@router.delete(
    "/{member_id}",
    status_code=200,
    responses={
        404: {"description": "Member is not part of the organization"},
        500: {"description": "Failed to remove member"},
    }
)
def remove_member(org_id: int, member_id: int, db: DbSession):
    try:
        return org_mem_service.remove_member(db, org_id, member_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logger.error("Failed to remove member %s from org %s", member_id, org_id)
        raise HTTPException(status_code=500, detail="Failed to remove member")