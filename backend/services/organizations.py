"""Business logic for Organizations"""

from sqlalchemy.orm import Session
from models import Organization, OrganizationMembers
import schema
from logger import get_logger

logger = get_logger(__name__)


def get_organization_by_id(org_id: int, db: Session):
    """Fetch organization by id"""
    return db.query(Organization).filter(Organization.id == org_id).first()


def get_organization_by_name(org_name: str, db: Session):
    """Fetch organization by name"""
    return db.query(Organization).filter(Organization.org_name == org_name).first()


def check_membership_by_user(user_id: int, db: Session):
    """Check if user belongs to any organization"""
    return (
        db.query(OrganizationMembers)
        .filter(OrganizationMembers.member_id == user_id)
        .first()
    )


def check_membership(user_id: int, org_id: int, db: Session):
    """Check if user is a member of a specific organization"""
    return (
        db.query(OrganizationMembers)
        .filter(
            OrganizationMembers.member_id == user_id,
            OrganizationMembers.organization_id == org_id,
        )
        .first()
    )


def create_organization(
    org: schema.OrganizationCreate, creator_id: int, db: Session
):
    """Creates organization and adds creator as first member"""
    try:
        new_org = Organization(org_name=org.org_name)
        db.add(new_org)
        db.flush()
        member = OrganizationMembers(
            member_id=creator_id,
            organization_id=new_org.id,
            role_id=1,
            added_by=creator_id,
        )
        db.add(member)
        db.commit()
        db.refresh(new_org)
        logger.info("Organization created: %s by user %s", new_org.org_name, creator_id)
        return new_org
    except Exception as e:
        db.rollback()
        logger.error("Failed to create organization: %s", e)
        raise
