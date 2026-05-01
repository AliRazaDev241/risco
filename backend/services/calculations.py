"""Pure financial calculations — no DB access, no models imported"""
from sqlalchemy import func, extract



def burn_rate(monthly_expenses: float) -> float:
    """
    Monthly cash burn — how much the organization spends per month.
    """
    return monthly_expenses


def cash_runway(cash_balance: float, monthly_expenses: float) -> float | None:
    """
    Months of cash remaining at current expense rate.
    Returns None if expenses are zero (undefined).
    If profitable, returns None to signal 'not applicable'.
    """
    if monthly_expenses <= 0:
        return None
    return cash_balance / monthly_expenses


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


def calculate_best(db, org_id: int, month: int, year: int) -> dict:
    """
    Best case projection:
    - Revenue: all expected revenue for the month (date_expected), not just received
    - Expenses: Non-Critical only (minimal spending scenario)
    """
    from models import Revenue, Expenses, Clients

    expected_amounts = [
        row.amount for row in db.query(Revenue).join(
            Clients, Revenue.client_id == Clients.id
        ).filter(
            Clients.organization_id == org_id,
            extract('month', Revenue.date_expected) == month,
            extract('year', Revenue.date_expected) == year
        ).all()
    ]

    non_critical_expenses = db.query(func.sum(Expenses.amount)).filter(
        Expenses.organization_id == org_id,
        Expenses.urgency == "Non-Critical",
        extract('month', Expenses.date) == month,
        extract('year', Expenses.date) == year
    ).scalar() or 0

    best_revenue = sum(expected_amounts)
    best_expenses = non_critical_expenses

    return {
        "monthly_revenue": best_revenue,
        "monthly_expense": best_expenses,
        "cash_balance": best_revenue - best_expenses,
        "concentration_risk": revenue_concentration_risk(expected_amounts),
    }


def calculate_worst(db, org_id: int, month: int, year: int) -> dict:
    """
    Worst case projection:
    - Revenue: reliable revenue only (weighted by client reliability scores)
    - Expenses: all expenses, Critical + Non-Critical
    """
    from models import Revenue, Expenses, Clients

    client_revenue = db.query(
        Revenue.amount,
        Clients.reliability_score
    ).join(
        Clients, Revenue.client_id == Clients.id
    ).filter(
        Clients.organization_id == org_id,
        extract('month', Revenue.date_expected) == month,
        extract('year', Revenue.date_expected) == year
    ).all()

    amounts = [row.amount for row in client_revenue]
    scores = [row.reliability_score for row in client_revenue]

    all_expenses = db.query(func.sum(Expenses.amount)).filter(
        Expenses.organization_id == org_id,
        extract('month', Expenses.date) == month,
        extract('year', Expenses.date) == year
    ).scalar() or 0

    worst_revenue = reliable_revenue(amounts, scores)
    worst_expenses = all_expenses

    return {
        "monthly_revenue": worst_revenue,
        "monthly_expense": worst_expenses,
        "cash_balance": worst_revenue - worst_expenses,
        "concentration_risk": revenue_concentration_risk(amounts),
    }