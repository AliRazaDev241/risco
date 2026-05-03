from sqlalchemy.orm import Session
from sqlalchemy import text
from logger import get_logger
from models import OrganizationMembers

logger = get_logger(__name__)


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
        raise LookupError(f"Member {member_id} not found in organization {org_id}")
    return member


def get_all_members(org_id: int, db: Session):
    query = text("""
        SELECT users.email, roles.role_name, organization_members.member_id
        FROM users
        JOIN organization_members ON users.id = organization_members.member_id
        JOIN roles ON organization_members.role_id = roles.id
        WHERE organization_members.organization_id = :org_id
    """)
    result = db.execute(query, {"org_id": org_id})
    rows = result.fetchall()
    logger.info("Fetched %s members for organization %s", len(rows), org_id)
    return [
        {"email": row.email, "role_name": row.role_name, "member_id": row.member_id}
        for row in rows
    ]


ASSIGNABLE_ROLES = {"coowner", "stakeholder"}


def add_member(org_id: int, email: str, role_name: str, added_by: int, db: Session):
    if role_name not in ASSIGNABLE_ROLES:
        raise ValueError(f"Cannot assign role '{role_name}' through this form")
    user_row = db.execute(
        text("SELECT id FROM users WHERE email = :email"), {"email": email}
    ).fetchone()
    if not user_row:
        raise LookupError(f"No user found with email {email}")
    member_id = user_row.id

    role_row = db.execute(
        text("SELECT id FROM roles WHERE role_name = :role_name"),
        {"role_name": role_name},
    ).fetchone()
    if not role_row:
        raise LookupError(f"No role found with name {role_name}")
    role_id = role_row.id

    already_exists = (
        db.query(OrganizationMembers)
        .filter(
            OrganizationMembers.member_id == member_id,
            OrganizationMembers.organization_id == org_id,
        )
        .first()
    )
    if already_exists:
        raise ValueError(f"{email} is already a member of this organization")

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
        raise


def remove_member(db: Session, org_id: int, member_id: int) -> dict:
    member = get_member(db, org_id, member_id)
    db.delete(member)
    db.commit()
    logger.info("Member %s removed from org %s", member_id, org_id)
    return {"detail": f"Member {member_id} removed from organization {org_id}"}
