"""Test cases for services/calculations.py"""

import pytest
from services import calculations


def test_revenue_reliability_score_basic():
    amounts = [1000.0, 500.0]
    scores = [80, 60]
    result = calculations.revenue_reliability_score(amounts, scores)
    assert result == pytest.approx(73.33, rel=1e-2)


def test_revenue_reliability_score_zero_amounts():
    result = calculations.revenue_reliability_score([0.0, 0.0], [80, 60])
    assert result == pytest.approx(0.0)


def test_revenue_reliability_score_mismatched_lengths_raises():
    with pytest.raises(ValueError):
        calculations.revenue_reliability_score([1000.0], [80, 60])


def test_revenue_reliability_score_single_client():
    result = calculations.revenue_reliability_score([5000.0], [90])
    assert result == pytest.approx(90.0)


def test_revenue_concentration_risk_single_client():
    result = calculations.revenue_concentration_risk([5000.0])
    assert result == pytest.approx(1.0)


def test_revenue_concentration_risk_equal_clients():
    result = calculations.revenue_concentration_risk([500.0, 500.0])
    assert result == pytest.approx(0.5)


def test_revenue_concentration_risk_zero_amounts():
    result = calculations.revenue_concentration_risk([0.0, 0.0])
    assert result == pytest.approx(0.0)


def test_revenue_concentration_risk_multiple_clients():
    result = calculations.revenue_concentration_risk([250.0, 250.0, 250.0, 250.0])
    assert result == pytest.approx(0.25, rel=1e-2)


def test_reliable_revenue_basic():
    result = calculations.reliable_revenue([1000.0, 500.0], [80, 60])
    assert result == pytest.approx(1100.0)


def test_reliable_revenue_zero_scores():
    result = calculations.reliable_revenue([1000.0, 500.0], [0, 0])
    assert result == pytest.approx(0.0)


def test_reliable_revenue_full_scores():
    result = calculations.reliable_revenue([1000.0, 500.0], [100, 100])
    assert result == pytest.approx(1500.0)


def test_reliable_revenue_mismatched_lengths_raises():
    with pytest.raises(ValueError):
        calculations.reliable_revenue([1000.0], [80, 60])


def test_total_revenue_basic():
    result = calculations.total_revenue([1000.0, 500.0, 250.0])
    assert result == pytest.approx(1750.0)


def test_total_revenue_empty():
    result = calculations.total_revenue([])
    assert result == pytest.approx(0.0)


def test_cash_runway_basic():
    result = calculations.cash_runway(10000.0, 2000.0)
    assert result == pytest.approx(5.0)


def test_cash_runway_zero_expenses_returns_none():
    result = calculations.cash_runway(10000.0, 0.0)
    assert result is None


def test_cash_runway_negative_expenses_returns_none():
    result = calculations.cash_runway(10000.0, -500.0)
    assert result is None


def test_cash_balance_basic():
    result = calculations.cash_balance(5000.0, 3000.0, 1000.0)
    assert result == pytest.approx(7000.0)


def test_cash_balance_no_previous_balance():
    result = calculations.cash_balance(None, 3000.0, 1000.0)
    assert result == pytest.approx(2000.0)


def test_cash_balance_negative_previous_treated_as_zero():
    result = calculations.cash_balance(-500.0, 3000.0, 1000.0)
    assert result == pytest.approx(2000.0)