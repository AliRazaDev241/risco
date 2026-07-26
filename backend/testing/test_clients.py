"""Test cases for services/clients.py"""

import pytest
from unittest.mock import MagicMock
from services import clients as client_service
import schema

# ── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def mock_db():
    """Mock database session so no real DB connection is needed"""
    return MagicMock()


@pytest.fixture
def sample_client():
    client = MagicMock()
    client.id = 1
    client.organization_id = 10
    client.name = "Ali Corp"
    client.email = "ali@corp.com"
    client.contact_number = "03001234567"
    client.reliability_score = 80
    return client


# ── add_client ───────────────────────────────────────────────────────────────


def test_add_client_success(mock_db, sample_client):
    mock_db.refresh = MagicMock()
    client_data = schema.ClientsCreate(
        organization_id=10,
        name="Ali Corp",
        email="ali@corp.com",
        contact_number="03001234567",
        reliability_score=80,
    )
    client_service.add_client(client_data, mock_db)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_add_client_without_contact_number(mock_db):
    mock_db.refresh = MagicMock()
    client_data = schema.ClientsCreate(
        organization_id=10,
        name="No Phone Client",
        email="nophone@corp.com",
        contact_number=None,
        reliability_score=70,
    )
    client_service.add_client(client_data, mock_db)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.xfail(reason="[SEVERITY: High] — Missing reliability_score on client creation")
def test_add_client_returns_new_client(mock_db, sample_client):
    mock_db.refresh = MagicMock()
    mock_db.add = MagicMock()
    client_data = schema.ClientsCreate(
        organization_id=10,
        name="Ali Corp",
        email="ali@corp.com",
        contact_number="03001234567",
        reliability_score=80,
    )
    client_service.add_client(client_data, mock_db)
    created = mock_db.add.call_args[0][0]
    assert created.name == "Ali Corp"
    assert created.email == "ali@corp.com"
    assert created.organization_id == 10
    assert created.reliability_score == 80


def test_add_client_db_commit(mock_db):
    mock_db.refresh = MagicMock()
    client_data = schema.ClientsCreate(
        organization_id=10,
        name="Ali Corp",
        email="ali@corp.com",
        contact_number="03001234567",
        reliability_score=80,
    )
    client_service.add_client(client_data, mock_db)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_add_client_db_failure_rolls_back(mock_db):
    client_data = schema.ClientsCreate(
        organization_id=10,
        name="Fail Corp",
        email="fail@corp.com",
        contact_number=None,
        reliability_score=70,
    )
    mock_db.commit.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        client_service.add_client(client_data, mock_db)
    mock_db.rollback.assert_called_once()

# ── update_reliability_score ──────────────────────────────────────────────────

def test_update_reliability_score_success(mock_db):
    # Mocking db.execute to return total = 4, received = 3
    # Note: the function executes two queries if total > 0.
    mock_db.execute.return_value.scalar.side_effect = [4, 3]
    
    client_service.update_reliability_score(mock_db, 1)
    
    # 3/4 = 75%
    assert mock_db.execute.call_count == 3
    mock_db.commit.assert_called_once()

def test_update_reliability_score_zero_total(mock_db):
    mock_db.execute.return_value.scalar.return_value = 0
    client_service.update_reliability_score(mock_db, 1)
    
    # Should return early, only 1 execute call and no commit
    assert mock_db.execute.call_count == 1
    mock_db.commit.assert_not_called()

# ── recalculate_reliability ───────────────────────────────────────────────────

def test_recalculate_reliability_no_history(mock_db):
    mock_db.execute.return_value.fetchall.return_value = []
    score = client_service.recalculate_reliability(mock_db, 1)
    assert score == 100

def test_recalculate_reliability_with_history(mock_db):
    row1 = MagicMock(days_late=0)
    row2 = MagicMock(days_late=45) # 0.5 contribution
    row3 = MagicMock(days_late=90) # 0.0 contribution
    mock_db.execute.return_value.fetchall.return_value = [row1, row2, row3]
    
    # average of (1.0, 0.5, 0.0) = 0.5 -> 50%
    score = client_service.recalculate_reliability(mock_db, 1)
    assert score == 50

