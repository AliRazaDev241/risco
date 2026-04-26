from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from fastapi import HTTPException, status

from models import OrganizationMembers, Users, Organization, Roles


def get_all_members(db: Session, org_id: int):
    query = text("""
        SELECT users.email, roles.role_name
        FROM users
        JOIN organization_members ON users.id = organization_members.member_id
        JOIN roles ON organization_members.role_id = roles.id
        WHERE organization_members.organization_id = :org_id
    """)
    result = db.execute(query, {"org_id": org_id})
    rows = result.fetchall()
    return [{"email": row.email, "role_name": row.role_name} for row in rows]

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


def add_member(db: Session, org_id: int, member_id: int, role_id: int, added_by: int) -> OrganizationMembers:
    # Verify org exists
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization {org_id} not found",
        )

    # Verify user being added exists
    user = db.query(Users).filter(Users.id == member_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {member_id} not found",
        )

    # Verify role exists
    role = db.query(Roles).filter(Roles.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role {role_id} not found",
        )

    # Verify added_by user exists
    adder = db.query(Users).filter(Users.id == added_by).first()
    if not adder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {added_by} (added_by) not found",
        )

    # Check already a member
    existing = (
        db.query(OrganizationMembers)
        .filter(
            OrganizationMembers.organization_id == org_id,
            OrganizationMembers.member_id == member_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {member_id} is already a member of organization {org_id}",
        )

    member = OrganizationMembers(
        organization_id=org_id,
        member_id=member_id,
        role_id=role_id,
        added_by=added_by,
    )

    try:
        db.add(member)
        db.commit()
        db.refresh(member)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add member due to a database constraint violation",
        )

    return member

def remove_member(db: Session, org_id: int, member_id: int) -> dict:
    member = get_member(db, org_id, member_id)
    db.delete(member)
    db.commit()
    return {"detail": f"Member {member_id} removed from organization {org_id}"}