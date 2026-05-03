"""Test cases for services/users.py"""

import pytest
from unittest.mock import MagicMock, patch
from services import auth as user_service
import schema
import os

# ── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def mock_db():
    """Mock database session so no real DB connection is needed"""
    return MagicMock()


@pytest.fixture
def sample_user():
    user = MagicMock()
    user.id = 1
    user.email = "ali@risco.com"
    user.password_hash = user_service.hash_password("pass123")
    user.first_name = "Ali"
    user.last_name = "Raza"
    return user


# ── hash_password ────────────────────────────────────────────────────────────


def test_hash_password_returns_string():
    assert isinstance(user_service.hash_password("mypassword"), str)


def test_hash_password_is_not_plaintext():
    assert user_service.hash_password("mypassword") != "mypassword"


def test_hash_password_different_hashes_same_input():
    assert user_service.hash_password("mypassword") != user_service.hash_password("mypassword")


# ── verify_password ──────────────────────────────────────────────────────────


def test_verify_password_correct():
    hashed = user_service.hash_password("secure123")
    assert user_service.verify_password("secure123", hashed) is True


def test_verify_password_wrong():
    hashed = user_service.hash_password("secure123")
    assert user_service.verify_password("wrongpass", hashed) is False


# ── get_user_by_email ────────────────────────────────────────────────────────


def test_get_user_by_email_found(mock_db, sample_user):
    mock_db.query().filter().first.return_value = sample_user
    assert user_service.get_user_by_email("ali@risco.com", mock_db).email == "ali@risco.com"


def test_get_user_by_email_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    assert user_service.get_user_by_email("ghost@risco.com", mock_db) is None


# ── get_user_by_id ───────────────────────────────────────────────────────────


def test_get_user_by_id_found(mock_db, sample_user):
    mock_db.query().filter().first.return_value = sample_user
    assert user_service.get_user_by_id(1, mock_db).id == 1


def test_get_user_by_id_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    assert user_service.get_user_by_id(999, mock_db) is None


# ── create_user ──────────────────────────────────────────────────────────────


def test_create_user_success(mock_db):
    user_data = schema.UserCreate(
        email="new@risco.com",
        password=os.getenv("TEST_USER_PASSWORD"),
        first_name="New",
        last_name="User",
    )
    mock_db.refresh = MagicMock()
    user_service.create_user(user_data, mock_db)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_create_user_password_is_hashed(mock_db):
    user_data = schema.UserCreate(
        email="new@risco.com",
        password=os.getenv("TEST_USER_PASSWORD"),
        first_name="New",
        last_name="User",
    )
    mock_db.refresh = MagicMock()
    user_service.create_user(user_data, mock_db)
    assert mock_db.add.call_args[0][0].password_hash != "plaintext"


def test_create_user_db_failure_rolls_back(mock_db):
    mock_db.commit.side_effect = Exception("DB error")
    user_data = schema.UserCreate(
        email="fail@risco.com",
        password=os.getenv("TEST_USER_PASSWORD"),
        first_name="Fail",
        last_name="User",
    )
    with pytest.raises(Exception):
        user_service.create_user(user_data, mock_db)
    mock_db.rollback.assert_called_once()


# ── authenticate_user ────────────────────────────────────────────────────────


def test_authenticate_user_success(mock_db, sample_user):
    real_hash = user_service.hash_password("secure123")
    sample_user.password_hash = real_hash
    mock_db.query().filter().first.return_value = sample_user
    assert user_service.authenticate_user("ali@risco.com", "secure123", mock_db) is not None


def test_authenticate_user_wrong_password(mock_db, sample_user):
    mock_db.query().filter().first.return_value = sample_user
    assert user_service.authenticate_user("ali@risco.com", "wrongpass", mock_db) is None


def test_authenticate_user_email_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    assert user_service.authenticate_user("nobody@risco.com", "pass", mock_db) is None