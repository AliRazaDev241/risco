from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from fastapi import HTTPException, status
from logger import get_logger

logger = get_logger(__name__)

from models import OrganizationMembers, Users, Organization, Roles


def get_member(db: Session, org_id: int, member_id: int) -> OrganizationMembers:
    member = (
        db.query(OrganizationMembers)
        .filter(
            OrganizationMembers.organization_id == org_id,
            OrganizationMembers.member_id == member_id,
        )
        .first()
    )
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member {member_id} not found in organization {org_id}",
        )
    return member


def get_all_members(org_id: int, db: Session):
    """Fetch all members of an org with email and role name"""
    query = text("""
        SELECT users.email, roles.role_name
        FROM users
        JOIN organization_members ON users.id = organization_members.member_id
        JOIN roles ON organization_members.role_id = roles.id
        WHERE organization_members.organization_id = :org_id
    """)
    result = db.execute(query, {"org_id": org_id})
    rows = result.fetchall()
    logger.info("Fetched %s members for organization %s", len(rows), org_id)
    return [{"email": row.email, "role_name": row.role_name} for row in rows]


def add_member(org_id: int, email: str, role_name: str, added_by: int, db: Session):
    """Add a member to an org by email and role name"""

    # Look up user by email
    user_row = db.execute(
        text("SELECT id FROM users WHERE email = :email"), {"email": email}
    ).fetchone()
    if not user_row:
        logger.warning("Add member failed — email not found: %s", email)
        raise HTTPException(status_code=404, detail=f"No user found with email {email}")

    member_id = user_row.id

    # Look up role by name
    role_row = db.execute(
        text("SELECT id FROM roles WHERE role_name = :role_name"),
        {"role_name": role_name},
    ).fetchone()
    if not role_row:
        logger.warning("Add member failed — role not found: %s", role_name)
        raise HTTPException(
            status_code=404, detail=f"No role found with name {role_name}"
        )

    role_id = role_row.id

    # Check already a member
    already_exists = (
        db.query(OrganizationMembers)
        .filter(
            OrganizationMembers.member_id == member_id,
            OrganizationMembers.organization_id == org_id,
        )
        .first()
    )
    if already_exists:
        logger.warning(
            "Add member failed — user %s already in org %s", member_id, org_id
        )
        raise HTTPException(
            status_code=409, detail=f"{email} is already a member of this organization"
        )

    # Insert via ORM — lets SQLAlchemy handle Oracle identifier quoting
    try:
        member = OrganizationMembers(
            member_id=member_id,
            organization_id=org_id,
            role_id=role_id,
            added_by=added_by,
        )
        db.add(member)
        db.commit()
        db.refresh(member)
        logger.info(
            "Member %s added to org %s with role %s by user %s",
            email,
            org_id,
            role_name,
            added_by,
        )
        return {"detail": f"{email} added successfully as {role_name}"}
    except Exception as e:
        db.rollback()
        logger.error("Failed to add member %s to org %s: %s", email, org_id, e)
        raise HTTPException(status_code=500, detail="Failed to add member")


def remove_member(db: Session, org_id: int, member_id: int) -> dict:
    member = get_member(db, org_id, member_id)
    db.delete(member)
    db.commit()
    return {"detail": f"Member {member_id} removed from organization {org_id}"}
