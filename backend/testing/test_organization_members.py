"""Test cases for services/organization_members.py"""

import pytest
from unittest.mock import MagicMock
from services import organization_members as member_service

# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def mock_db():
    """Mock database session so no real DB connection is needed"""
    return MagicMock()


@pytest.fixture
def sample_member():
    member = MagicMock()
    member.member_id = 10
    member.organization_id = 1
    member.role_id = 2
    member.added_by = 99
    return member


# ── get_member ────────────────────────────────────────────────────────────────


def test_get_member_found(mock_db, sample_member):
    mock_db.query().filter().first.return_value = sample_member
    result = member_service.get_member(mock_db, org_id=1, member_id=10)
    assert result.member_id == 10


def test_get_member_not_found_raises(mock_db):
    mock_db.query().filter().first.return_value = None
    with pytest.raises(LookupError, match="Member 999 not found"):
        member_service.get_member(mock_db, org_id=1, member_id=999)


# ── get_all_members ───────────────────────────────────────────────────────────


def test_get_all_members_returns_list(mock_db):
    row1 = MagicMock()
    row1.email = "alice@risco.com"
    row1.role_name = "admin"
    row2 = MagicMock()
    row2.email = "bob@risco.com"
    row2.role_name = "viewer"
    mock_db.execute.return_value.fetchall.return_value = [row1, row2]

    result = member_service.get_all_members(org_id=1, db=mock_db)

    assert len(result) == 2
    assert result[0] == {"email": "alice@risco.com", "role_name": "admin"}
    assert result[1] == {"email": "bob@risco.com", "role_name": "viewer"}


def test_get_all_members_empty_org(mock_db):
    mock_db.execute.return_value.fetchall.return_value = []
    result = member_service.get_all_members(org_id=99, db=mock_db)
    assert result == []


# ── add_member ────────────────────────────────────────────────────────────────


def test_add_member_success(mock_db):
    user_row = MagicMock()
    user_row.id = 10
    role_row = MagicMock()
    role_row.id = 2

    mock_db.execute.return_value.fetchone.side_effect = [user_row, role_row]
    mock_db.query().filter().first.return_value = None
    mock_db.refresh = MagicMock()

    result = member_service.add_member(
        org_id=1,
        email="alice@risco.com",
        role_name="admin",
        added_by=99,
        db=mock_db,
    )

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    assert "added successfully" in result["detail"]


def test_add_member_user_not_found_raises(mock_db):
    mock_db.execute.return_value.fetchone.return_value = None

    with pytest.raises(LookupError, match="No user found"):
        member_service.add_member(
            org_id=1,
            email="ghost@risco.com",
            role_name="admin",
            added_by=99,
            db=mock_db,
        )


def test_add_member_role_not_found_raises(mock_db):
    user_row = MagicMock()
    user_row.id = 10
    mock_db.execute.return_value.fetchone.side_effect = [user_row, None]

    with pytest.raises(LookupError, match="No role found"):
        member_service.add_member(
            org_id=1,
            email="alice@risco.com",
            role_name="ghost_role",
            added_by=99,
            db=mock_db,
        )


def test_add_member_already_exists_raises(mock_db, sample_member):
    user_row = MagicMock()
    user_row.id = 10
    role_row = MagicMock()
    role_row.id = 2
    mock_db.execute.return_value.fetchone.side_effect = [user_row, role_row]
    mock_db.query().filter().first.return_value = sample_member

    with pytest.raises(ValueError, match="already a member"):
        member_service.add_member(
            org_id=1,
            email="alice@risco.com",
            role_name="admin",
            added_by=99,
            db=mock_db,
        )


def test_add_member_db_failure_rolls_back(mock_db):
    user_row = MagicMock()
    user_row.id = 10
    role_row = MagicMock()
    role_row.id = 2
    mock_db.execute.return_value.fetchone.side_effect = [user_row, role_row]
    mock_db.query().filter().first.return_value = None
    mock_db.commit.side_effect = Exception("DB error")

    with pytest.raises(Exception):
        member_service.add_member(
            org_id=1,
            email="alice@risco.com",
            role_name="admin",
            added_by=99,
            db=mock_db,
        )
    mock_db.rollback.assert_called_once()


# ── remove_member ─────────────────────────────────────────────────────────────


def test_remove_member_success(mock_db, sample_member):
    mock_db.query().filter().first.return_value = sample_member

    result = member_service.remove_member(mock_db, org_id=1, member_id=10)

    mock_db.delete.assert_called_once_with(sample_member)
    mock_db.commit.assert_called_once()
    assert "removed" in result["detail"]


def test_remove_member_not_found_raises(mock_db):
    mock_db.query().filter().first.return_value = None

    with pytest.raises(LookupError, match="Member 999 not found"):
        member_service.remove_member(mock_db, org_id=1, member_id=999)
