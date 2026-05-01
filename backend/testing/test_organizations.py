"""Test cases for services/organizations.py"""

import pytest
from unittest.mock import MagicMock, patch
from services import organizations as org_service
import schema


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def mock_db():
    """Mock database session so no real DB connection is needed"""
    return MagicMock()


@pytest.fixture
def sample_org():
    org = MagicMock()
    org.id = 1
    org.org_name = "Risco Inc"
    return org


@pytest.fixture
def sample_member():
    member = MagicMock()
    member.member_id = 42
    member.organization_id = 1
    return member


# ── get_organization_by_id ────────────────────────────────────────────────────


def test_get_organization_by_id_found(mock_db, sample_org):
    mock_db.query().filter().first.return_value = sample_org
    result = org_service.get_organization_by_id(1, mock_db)
    assert result.id == 1


def test_get_organization_by_id_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    result = org_service.get_organization_by_id(999, mock_db)
    assert result is None


# ── get_organization_by_name ──────────────────────────────────────────────────


def test_get_organization_by_name_found(mock_db, sample_org):
    mock_db.query().filter().first.return_value = sample_org
    result = org_service.get_organization_by_name("Risco Inc", mock_db)
    assert result.org_name == "Risco Inc"


def test_get_organization_by_name_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    result = org_service.get_organization_by_name("Ghost Corp", mock_db)
    assert result is None


# ── check_membership_by_user ──────────────────────────────────────────────────


def test_check_membership_by_user_found(mock_db, sample_member):
    mock_db.query().filter().first.return_value = sample_member
    result = org_service.check_membership_by_user(42, mock_db)
    assert result.member_id == 42


def test_check_membership_by_user_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    result = org_service.check_membership_by_user(999, mock_db)
    assert result is None


# ── check_membership ──────────────────────────────────────────────────────────


def test_check_membership_found(mock_db, sample_member):
    mock_db.query().filter().first.return_value = sample_member
    result = org_service.check_membership(42, 1, mock_db)
    assert result.organization_id == 1


def test_check_membership_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    result = org_service.check_membership(42, 99, mock_db)
    assert result is None


# ── create_organization ───────────────────────────────────────────────────────


def test_create_organization_success(mock_db):
    org_data = schema.OrganizationCreate(org_name="Risco Inc")
    mock_db.refresh = MagicMock()

    result = org_service.create_organization(org_data, creator_id=1, db=mock_db)

    assert mock_db.add.call_count == 2  # once for org, once for member
    mock_db.flush.assert_called_once()
    mock_db.commit.assert_called_once()


def test_create_organization_adds_creator_as_member(mock_db):
    org_data = schema.OrganizationCreate(org_name="Risco Inc")
    mock_db.refresh = MagicMock()

    with patch("services.organizations.OrganizationMembers") as MockMember:
        org_service.create_organization(org_data, creator_id=5, db=mock_db)

        _, kwargs = MockMember.call_args
        assert kwargs["member_id"] == 5
        assert kwargs["role_id"] == 1
        assert kwargs["added_by"] == 5


def test_create_organization_db_failure_rolls_back(mock_db):
    org_data = schema.OrganizationCreate(org_name="Fail Corp")
    mock_db.commit.side_effect = Exception("DB error")

    with pytest.raises(Exception):
        org_service.create_organization(org_data, creator_id=1, db=mock_db)

    mock_db.rollback.assert_called_once()