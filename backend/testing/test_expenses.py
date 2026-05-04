"""Test cases for services/expenses.py"""

import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone
from services import expenses as expense_service
import schema


# ── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def mock_db():
    """Mock database session so no real DB connection is needed"""
    return MagicMock()


@pytest.fixture
def sample_expense_data():
    return schema.ExpenseCreate(
        organization_id=1,
        urgency="Critical",
        expense_type="One_Time",
        date=datetime(2024, 1, 15, tzinfo=timezone.utc),
        amount=5000,
    )


# ── add_expense ──────────────────────────────────────────────────────────────


def test_add_expense_success(mock_db, sample_expense_data):
    mock_db.execute.return_value.fetchone.return_value = (1,)
    mock_db.refresh = MagicMock()
    expense_service.add_expense(sample_expense_data, mock_db)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_add_expense_org_not_found(mock_db, sample_expense_data):
    mock_db.execute.return_value.fetchone.return_value = None
    with pytest.raises(LookupError):
        expense_service.add_expense(sample_expense_data, mock_db)


def test_add_expense_db_failure_rolls_back(mock_db, sample_expense_data):
    mock_db.execute.return_value.fetchone.return_value = (1,)
    mock_db.commit.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        expense_service.add_expense(sample_expense_data, mock_db)
    mock_db.rollback.assert_called_once()


def test_add_expense_does_not_commit_when_org_missing(mock_db, sample_expense_data):
    mock_db.execute.return_value.fetchone.return_value = None
    with pytest.raises(LookupError):
        expense_service.add_expense(sample_expense_data, mock_db)
    mock_db.commit.assert_not_called()


# ── list_five_expenses ───────────────────────────────────────────────────────


def test_list_five_expenses_success(mock_db):
    mock_db.execute.return_value.fetchone.return_value = (1,)
    mock_db.execute.return_value.scalar.return_value = 10
    mock_db.execute.return_value.fetchall.return_value = [
        ("Critical", "One_Time", datetime(2024, 1, 15), 5000)
    ]
    result = expense_service.list_five_expenses(1, "One_Time", 1, mock_db)
    assert "items" in result
    assert "total_pages" in result
    assert "current_page" in result


def test_list_five_expenses_org_not_found(mock_db):
    mock_db.execute.return_value.fetchone.return_value = None
    with pytest.raises(LookupError):
        expense_service.list_five_expenses(999, "One_Time", 1, mock_db)


def test_list_five_expenses_correct_page_returned(mock_db):
    mock_db.execute.return_value.fetchone.return_value = (1,)
    mock_db.execute.return_value.scalar.return_value = 10
    mock_db.execute.return_value.fetchall.return_value = []
    assert expense_service.list_five_expenses(1, "One_Time", 2, mock_db)["current_page"] == 2


def test_list_five_expenses_total_pages_calculated(mock_db):
    mock_db.execute.return_value.fetchone.return_value = (1,)
    mock_db.execute.return_value.scalar.return_value = 10
    mock_db.execute.return_value.fetchall.return_value = []
    assert expense_service.list_five_expenses(1, "One_Time", 1, mock_db)["total_pages"] == 2


def test_list_five_expenses_empty_returns_one_page(mock_db):
    mock_db.execute.return_value.fetchone.return_value = (1,)
    mock_db.execute.return_value.scalar.return_value = 0
    mock_db.execute.return_value.fetchall.return_value = []
    assert expense_service.list_five_expenses(1, "One_Time", 1, mock_db)["total_pages"] == 1