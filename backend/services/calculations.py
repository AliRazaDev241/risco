"""Pure financial calculations"""

from sqlalchemy import func, extract

def revenue_reliability_score(amounts: list[float], reliability_scores: list[int]) -> float:
    """
    Weighted average reliability score across all clients, weighted by revenue.
    Returns 0-100. Higher = your revenue comes from more reliable clients.

    amounts: list of revenue amounts per client
    reliability_scores: list of scores (0-100) matching amounts by index
    """
    if len(amounts) != len(reliability_scores):
        raise ValueError("amounts and reliability_scores must be the same length")
    total = sum(amounts)
    if total == 0:
        return 0.0
    return sum(a * s for a, s in zip(amounts, reliability_scores)) / total

def revenue_concentration_risk(amounts: list[float]) -> float:
    """
    Herfindahl-Hirschman Index (HHI) — measures how concentrated revenue is.
    Returns 0.0 to 1.0 where:
        ~0.0 = revenue evenly spread across many clients (low risk)
         1.0 = all revenue from one client (maximum risk)

    amounts: list of revenue amounts per client
    """
    total = sum(amounts)
    if total == 0:
        return 0.0
    shares = [a / total for a in amounts]
    return sum(s ** 2 for s in shares)

def reliable_revenue(amounts: list[float], reliability_scores: list[int]) -> float:
    """
    Revenue weighted by client reliability scores.
    reliable_revenue = sum(amount * score / 100) per client.
    Represents how much of your revenue you can actually count on.

    amounts: list of revenue amounts per client
    reliability_scores: list of scores (0-100) matching amounts by index
    """
    if len(amounts) != len(reliability_scores):
        raise ValueError("amounts and reliability_scores must be the same length")
    return sum(a * (s / 100) for a, s in zip(amounts, reliability_scores))

def total_revenue(amounts: list[float]) -> float:
    """Sum of all expected revenue amounts for the period."""
    return sum(amounts)

def cash_runway(cash_balance: float, monthly_expenses: float) -> float | None:
    """
    Months of cash remaining at current expense rate.
    Returns None if expenses are zero
    If profitable, returns None to signal 'not applicable'.
    """
    if monthly_expenses <= 0:
        return None
    return cash_balance / monthly_expenses


def cash_balance(cash_balance_previous: float | None, monthly_revenue: float, monthly_expenses: float) -> float:
    """
    Current cash balance.
    Previous balance + revenue received this month - expenses this month.
    If no previous balance exists (first month), starts from 0.
    """
    previous = cash_balance_previous if (cash_balance_previous is not None and cash_balance_previous >= 0) else 0.0
    return previous + monthly_revenue - monthly_expenses
