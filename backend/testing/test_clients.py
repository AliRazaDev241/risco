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
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
