"""Test cases for services/revenue.py"""

import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone
from services import revenue as revenue_service
import schema

# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def mock_db():
    """Mock database session so no real DB connection is needed"""
    return MagicMock()


@pytest.fixture
def sample_revenue():
    revenue = MagicMock()
    revenue.id = 1
    revenue.client_id = 10
    revenue.revenue_type = "One_Time"
    revenue.date_expected = datetime(2025, 6, 1, tzinfo=timezone.utc)
    revenue.date_received = None
    revenue.amount = 5000
    return revenue


@pytest.fixture
def sample_revenue_create():
    return schema.RevenueCreate(
        org_id=1,
        client_name="Acme Corp",
        revenue_type="One_Time",
        date_expected=datetime(2025, 6, 1, tzinfo=timezone.utc),
        date_received=None,
        amount=5000,
    )


# ── add_revenue ───────────────────────────────────────────────────────────────


def test_add_revenue_success(mock_db, sample_revenue_create):
    client_row = MagicMock()
    client_row.id = 10
    mock_db.execute.return_value.fetchone.return_value = client_row
    mock_db.refresh = MagicMock()

    revenue_service.add_revenue(sample_revenue_create, mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_add_revenue_client_not_found_raises(mock_db, sample_revenue_create):
    mock_db.execute.return_value.fetchone.return_value = None

    with pytest.raises(LookupError, match="No client found with name Acme Corp"):
        revenue_service.add_revenue(sample_revenue_create, mock_db)


def test_add_revenue_db_failure_rolls_back(mock_db, sample_revenue_create):
    client_row = MagicMock()
    client_row.id = 10
    mock_db.execute.return_value.fetchone.return_value = client_row
    mock_db.commit.side_effect = Exception("DB error")

    with pytest.raises(Exception):
        revenue_service.add_revenue(sample_revenue_create, mock_db)

    mock_db.rollback.assert_called_once()


# ── list_five_revenue ─────────────────────────────────────────────────────────


def test_list_five_revenue_success(mock_db):
    org_row = MagicMock()

    row1 = MagicMock()
    row1.id = 1
    row1.client_name = "Acme Corp"
    row1.client_email = "acme@corp.com"
    row1.date_expected = datetime(2025, 6, 1, tzinfo=timezone.utc)
    row1.date_received = None
    row1.amount = 5000

    mock_db.execute.return_value.fetchone.side_effect = [org_row]
    mock_db.execute.return_value.scalar.return_value = 1
    mock_db.execute.return_value.fetchall.return_value = [row1]

    result = revenue_service.list_five_revenue(
        org_id=1, revenue_type="One_Time", page_no=1, db=mock_db
    )

    assert result["current_page"] == 1
    assert result["total_pages"] == 1
    assert len(result["items"]) == 1


def test_list_five_revenue_org_not_found_raises(mock_db):
    mock_db.execute.return_value.fetchone.return_value = None

    with pytest.raises(LookupError, match="No organization found"):
        revenue_service.list_five_revenue(
            org_id=999, revenue_type="One_Time", page_no=1, db=mock_db
        )


def test_list_five_revenue_empty_returns_empty_list(mock_db):
    org_row = MagicMock()
    mock_db.execute.return_value.fetchone.side_effect = [org_row]
    mock_db.execute.return_value.scalar.return_value = 0
    mock_db.execute.return_value.fetchall.return_value = []

    result = revenue_service.list_five_revenue(
        org_id=1, revenue_type="Recurring", page_no=1, db=mock_db
    )

    assert result["items"] == []
    assert result["total_pages"] == 1


def test_list_five_revenue_pagination(mock_db):
    org_row = MagicMock()
    mock_db.execute.return_value.fetchone.side_effect = [org_row]
    mock_db.execute.return_value.scalar.return_value = 12
    mock_db.execute.return_value.fetchall.return_value = []

    result = revenue_service.list_five_revenue(
        org_id=1, revenue_type="One_Time", page_no=2, db=mock_db
    )

    assert result["total_pages"] == 3
    assert result["current_page"] == 2


# ── update_revenue ────────────────────────────────────────────────────────────


def test_update_revenue_success(mock_db, sample_revenue):
    mock_db.get.return_value = sample_revenue
    mock_db.refresh = MagicMock()

    data = schema.RevenueUpdate(date_received=datetime(2025, 5, 1, tzinfo=timezone.utc))

    result = revenue_service.update_revenue(1, data, mock_db)

    assert sample_revenue.date_received == datetime(2025, 5, 1, tzinfo=timezone.utc)
    mock_db.commit.assert_called_once()


def test_update_revenue_not_found_raises(mock_db):
    mock_db.get.return_value = None

    data = schema.RevenueUpdate(date_received=datetime(2025, 5, 1, tzinfo=timezone.utc))

    with pytest.raises(LookupError, match="No revenue found with id 999"):
        revenue_service.update_revenue(999, data, mock_db)


def test_update_revenue_none_date_received_not_updated(mock_db, sample_revenue):
    mock_db.get.return_value = sample_revenue
    mock_db.refresh = MagicMock()
    original_date = sample_revenue.date_received

    data = schema.RevenueUpdate(date_received=None)

    revenue_service.update_revenue(1, data, mock_db)

    assert sample_revenue.date_received == original_date
    mock_db.commit.assert_called_once()
