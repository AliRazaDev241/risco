"""Test cases for services/snapshots.py"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from services import snapshots as snapshot_service

# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def mock_db():
    """Mock database session so no real DB connection is needed"""
    return MagicMock()


@pytest.fixture
def sample_snapshot():
    snapshot = MagicMock()
    snapshot.organization_id = 1
    snapshot.snapshot_type = "Base"
    snapshot.monthly_revenue = 5000
    snapshot.monthly_expense = 2000
    snapshot.cash_balance = 3000
    return snapshot


# ── get_range ─────────────────────────────────────────────────────────────────


def test_get_range_success(mock_db, sample_snapshot):
    org_row = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = org_row

    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    end = datetime(2025, 1, 31, tzinfo=timezone.utc)

    with patch("services.snapshots.FinancialSnapshots") as MockSnapshot:
        MockSnapshot.organization_id = 1
        MockSnapshot.snapshot_date = MagicMock()
        MockSnapshot.snapshot_date.__ge__ = MagicMock(return_value=True)
        MockSnapshot.snapshot_date.__le__ = MagicMock(return_value=True)
        mock_db.query().filter().order_by().all.return_value = [sample_snapshot]

        result = snapshot_service.get_range(
            org_id=1, start_date=start, end_date=end, db=mock_db
        )

    assert len(result) == 1
    assert result[0].snapshot_type == "Base"


def test_get_range_org_not_found_raises(mock_db):
    mock_db.execute.return_value.fetchone.return_value = None

    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    end = datetime(2025, 1, 31, tzinfo=timezone.utc)

    with pytest.raises(LookupError, match="No organization found"):
        snapshot_service.get_range(
            org_id=999, start_date=start, end_date=end, db=mock_db
        )


def test_get_range_empty_returns_empty_list(mock_db):
    org_row = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = org_row

    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    end = datetime(2025, 1, 31, tzinfo=timezone.utc)

    with patch("services.snapshots.FinancialSnapshots") as MockSnapshot:
        MockSnapshot.snapshot_date = MagicMock()
        MockSnapshot.snapshot_date.__ge__ = MagicMock(return_value=True)
        MockSnapshot.snapshot_date.__le__ = MagicMock(return_value=True)
        mock_db.query().filter().order_by().all.return_value = []

        result = snapshot_service.get_range(
            org_id=1, start_date=start, end_date=end, db=mock_db
        )

    assert result == []


# ── refresh_or_create ─────────────────────────────────────────────────────────


def test_refresh_or_create_calls_all_three_upserts(mock_db):
    with patch.object(snapshot_service, "_upsert_base") as mock_base, patch.object(
        snapshot_service, "_upsert_best"
    ) as mock_best, patch.object(snapshot_service, "_upsert_worst") as mock_worst:

        snapshot_service.refresh_or_create(db=mock_db, org_id=1)

        mock_base.assert_called_once_with(mock_db, 1)
        mock_best.assert_called_once_with(mock_db, 1)
        mock_worst.assert_called_once_with(mock_db, 1)


# ── _upsert_snapshot ──────────────────────────────────────────────────────────


def test_upsert_snapshot_creates_new_when_not_exists(mock_db):
    mock_db.query().filter().first.return_value = None

    with patch("services.snapshots.FinancialSnapshots") as MockSnapshot:
        snapshot_service._upsert_snapshot(
            db=mock_db,
            org_id=1,
            snapshot_type="Base",
            monthly_revenue=5000,
            monthly_expenses=2000,
        )

        MockSnapshot.assert_called_once()
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()


def test_upsert_snapshot_updates_existing(mock_db, sample_snapshot):
    mock_db.query().filter().first.return_value = sample_snapshot

    snapshot_service._upsert_snapshot(
        db=mock_db,
        org_id=1,
        snapshot_type="Base",
        monthly_revenue=8000,
        monthly_expenses=3000,
    )

    assert sample_snapshot.monthly_revenue == 8000
    assert sample_snapshot.monthly_expense == 3000
    assert sample_snapshot.cash_balance == 5000
    mock_db.add.assert_not_called()
    mock_db.commit.assert_called_once()


def test_upsert_snapshot_cash_balance_is_revenue_minus_expenses(mock_db):
    mock_db.query().filter().first.return_value = None

    with patch("services.snapshots.FinancialSnapshots") as MockSnapshot:
        snapshot_service._upsert_snapshot(
            db=mock_db,
            org_id=1,
            snapshot_type="Base",
            monthly_revenue=10000,
            monthly_expenses=4000,
        )

        _, kwargs = MockSnapshot.call_args
        assert kwargs["cash_balance"] == 6000


# ── _upsert_base ──────────────────────────────────────────────────────────────


def test_upsert_base_calls_upsert_snapshot(mock_db):
    mock_db.query().filter().scalar.side_effect = [2000, 5000]

    with patch.object(snapshot_service, "_upsert_snapshot") as mock_upsert:
        snapshot_service._upsert_base(db=mock_db, org_id=1)

        mock_upsert.assert_called_once()
        args, _ = mock_upsert.call_args
        assert args[2] == "Base"


# ── _upsert_best ──────────────────────────────────────────────────────────────


def test_upsert_best_calls_upsert_snapshot(mock_db):
    row1 = MagicMock()
    row1.amount = 3000
    row2 = MagicMock()
    row2.amount = 2000

    mock_db.execute.return_value.fetchall.return_value = [row1, row2]
    mock_db.execute.return_value.scalar.return_value = 1000

    with patch.object(snapshot_service, "_upsert_snapshot") as mock_upsert:
        snapshot_service._upsert_best(db=mock_db, org_id=1)

        mock_upsert.assert_called_once()
        args, _ = mock_upsert.call_args
        assert args[2] == "Best"
        assert args[3] == 5000


# ── _upsert_worst ─────────────────────────────────────────────────────────────


def test_upsert_worst_calls_upsert_snapshot(mock_db):
    row1 = MagicMock()
    row1.amount = 3000
    row1.reliability_score = 80
    row2 = MagicMock()
    row2.amount = 2000
    row2.reliability_score = 60

    mock_db.execute.return_value.fetchall.return_value = [row1, row2]
    mock_db.execute.return_value.scalar.return_value = 3000

    with patch.object(snapshot_service, "_upsert_snapshot") as mock_upsert, \
         patch("services.snapshots.reliable_revenue") as mock_reliable:
        mock_reliable.return_value = pytest.approx(3600.0)

        snapshot_service._upsert_worst(db=mock_db, org_id=1)

        mock_upsert.assert_called_once()
        args, _ = mock_upsert.call_args
        assert args[2] == "Worst"
        assert args[3] == pytest.approx(3600.0)