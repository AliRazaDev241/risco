"""Test cases for services/financial.py"""

import pytest
from unittest.mock import MagicMock, patch
from services import financial as financial_service


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def mock_db():
    """Mock database session so no real DB connection is needed"""
    return MagicMock()


# ── get_intelligence_metrics ──────────────────────────────────────────────────


def test_get_intelligence_metrics_success(mock_db):
    org_row = MagicMock()

    row1 = MagicMock()
    row1.amount = 1000.0
    row1.reliability_score = 80

    row2 = MagicMock()
    row2.amount = 500.0
    row2.reliability_score = 60

    mock_db.execute.return_value.fetchone.return_value = org_row
    mock_db.execute.return_value.fetchall.return_value = [row1, row2]
    mock_db.execute.return_value.scalar.return_value = 800.0

    with patch("services.financial.calculations") as mock_calc:
        mock_calc.revenue_reliability_score.return_value = 73.33
        mock_calc.revenue_concentration_risk.return_value = 0.56
        mock_calc.reliable_revenue.return_value = 1100.0
        mock_calc.total_revenue.return_value = 1500.0

        result = financial_service.get_intelligence_metrics(org_id=1, db=mock_db)

    assert result["revenue_reliability_score"] == pytest.approx(73.33)
    assert result["revenue_concentration_risk"] == pytest.approx(0.56)
    assert result["reliable_revenue"] == pytest.approx(1100.0)
    assert result["total_revenue_expected"] == pytest.approx(1500.0)
    assert result["actual_revenue"] == pytest.approx(800.0)


def test_get_intelligence_metrics_org_not_found_raises(mock_db):
    mock_db.execute.return_value.fetchone.return_value = None

    with pytest.raises(LookupError, match="No organization found"):
        financial_service.get_intelligence_metrics(org_id=999, db=mock_db)


def test_get_intelligence_metrics_no_revenue(mock_db):
    org_row = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = org_row
    mock_db.execute.return_value.fetchall.return_value = []
    mock_db.execute.return_value.scalar.return_value = 0.0

    with patch("services.financial.calculations") as mock_calc:
        mock_calc.revenue_reliability_score.return_value = 0.0
        mock_calc.revenue_concentration_risk.return_value = 0.0
        mock_calc.reliable_revenue.return_value = 0.0
        mock_calc.total_revenue.return_value = 0.0

        result = financial_service.get_intelligence_metrics(org_id=1, db=mock_db)

    assert result["total_revenue_expected"] == pytest.approx(0.0)
    assert result["actual_revenue"] == pytest.approx(0.0)


# ── get_dashboard_metrics ─────────────────────────────────────────────────────


def test_get_dashboard_metrics_success(mock_db):
    org_row = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = org_row
    mock_db.execute.return_value.scalar.side_effect = [5000.0, 2000.0, 10000.0, 10]

    with patch("services.financial.calculations") as mock_calc:
        mock_calc.cash_balance.return_value = 13000.0
        mock_calc.cash_runway.return_value = 6.5

        result = financial_service.get_dashboard_metrics(org_id=1, db=mock_db)

    assert result["cash_balance"] == pytest.approx(13000.0)
    assert result["cash_runway"] == pytest.approx(6.5)
    assert result["burn_rate"] == pytest.approx(2000.0)
    assert result["monthly_revenue"] == pytest.approx(5000.0)
    assert result["headcount"] == 10


def test_get_dashboard_metrics_org_not_found_raises(mock_db):
    mock_db.execute.return_value.fetchone.return_value = None

    with pytest.raises(LookupError, match="No organization found"):
        financial_service.get_dashboard_metrics(org_id=999, db=mock_db)


def test_get_dashboard_metrics_no_previous_snapshot(mock_db):
    org_row = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = org_row
    mock_db.execute.return_value.scalar.side_effect = [3000.0, 1000.0, None, 5]

    with patch("services.financial.calculations") as mock_calc:
        mock_calc.cash_balance.return_value = 2000.0
        mock_calc.cash_runway.return_value = 2.0

        result = financial_service.get_dashboard_metrics(org_id=1, db=mock_db)

    assert result["cash_balance"] == pytest.approx(2000.0)
    assert result["headcount"] == 5