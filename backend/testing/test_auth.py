"""Test cases for services/users.py"""

import pytest
from unittest.mock import MagicMock, patch
from services import auth as user_service
import schema

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
    user.password_hash = user_service.hash_password("pass123")  # short password
    user.first_name = "Ali"
    user.last_name = "Raza"
    return user


# ── hash_password ────────────────────────────────────────────────────────────


def test_hash_password_returns_string():
    result = user_service.hash_password("mypassword")
    assert isinstance(result, str)


def test_hash_password_is_not_plaintext():
    result = user_service.hash_password("mypassword")
    assert result != "mypassword"


def test_hash_password_different_hashes_same_input():
    """bcrypt generates unique salt each time so same input gives different hash"""
    h1 = user_service.hash_password("mypassword")
    h2 = user_service.hash_password("mypassword")
    assert h1 != h2


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
    result = user_service.get_user_by_email("ali@risco.com", mock_db)
    assert result.email == "ali@risco.com"


def test_get_user_by_email_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    result = user_service.get_user_by_email("ghost@risco.com", mock_db)
    assert result is None


# ── get_user_by_id ───────────────────────────────────────────────────────────


def test_get_user_by_id_found(mock_db, sample_user):
    mock_db.query().filter().first.return_value = sample_user
    result = user_service.get_user_by_id(1, mock_db)
    assert result.id == 1


def test_get_user_by_id_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    result = user_service.get_user_by_id(999, mock_db)
    assert result is None


# ── create_user ──────────────────────────────────────────────────────────────


def test_create_user_success(mock_db):
    # Change password_hash= to password= in all three create_user tests
    user_data = schema.UserCreate(
        email="new@risco.com",
        password="pass1234",  # not password_hash
        first_name="New",
        last_name="User",
    )
    mock_db.refresh = MagicMock()
    result = user_service.create_user(user_data, mock_db)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_create_user_password_is_hashed(mock_db):
    # Change password_hash= to password= in all three create_user tests
    user_data = schema.UserCreate(
        email="new@risco.com",
        password="pass1234",  # not password_hash
        first_name="New",
        last_name="User",
    )
    mock_db.refresh = MagicMock()
    user_service.create_user(user_data, mock_db)
    created = mock_db.add.call_args[0][0]
    assert created.password_hash != "plaintext"


def test_create_user_db_failure_rolls_back(mock_db):
    mock_db.commit.side_effect = Exception("DB error")
    user_data = schema.UserCreate(
        email="fail@risco.com", password="password123", first_name="Fail", last_name="User"
    )
    with pytest.raises(Exception):
        user_service.create_user(user_data, mock_db)
    mock_db.rollback.assert_called_once()


# ── authenticate_user ────────────────────────────────────────────────────────


def test_authenticate_user_success(mock_db, sample_user):
    real_hash = user_service.hash_password("secure123")
    sample_user.password_hash = real_hash  # set real hash, not mock attribute
    mock_db.query().filter().first.return_value = sample_user
    result = user_service.authenticate_user("ali@risco.com", "secure123", mock_db)
    assert result is not None


def test_authenticate_user_wrong_password(mock_db, sample_user):
    mock_db.query().filter().first.return_value = sample_user
    result = user_service.authenticate_user("ali@risco.com", "wrongpass", mock_db)
    assert result is None


def test_authenticate_user_email_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    result = user_service.authenticate_user("nobody@risco.com", "pass", mock_db)
    assert result is None
