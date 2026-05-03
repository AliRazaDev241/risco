"""Business logic for Financial Snapshots"""

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, text
from models import Revenue, Expenses, Clients, FinancialSnapshots
import schema
from services import calculations
from logger import get_logger

logger = get_logger(__name__)

def get_graph(snapshot: schema.GraphRequest, db):
    org = db.execute(
        text("SELECT id FROM organizations WHERE id = :org_id"),
        {"org_id": snapshot.org_id},
    ).fetchone()
    if not org:
        raise LookupError(f"No organization found with id {snapshot.org_id}")

    date_range = (
        db.query(
            func.min(FinancialSnapshots.snapshot_date),
            func.max(FinancialSnapshots.snapshot_date),
        )
        .filter(
            FinancialSnapshots.organization_id == snapshot.org_id,
            FinancialSnapshots.snapshot_type == snapshot.snapshot_type,
        )
        .one()
    )

    rows = (
        db.query(FinancialSnapshots)
        .filter(
            FinancialSnapshots.organization_id == snapshot.org_id,
            FinancialSnapshots.snapshot_type == snapshot.snapshot_type,
            FinancialSnapshots.snapshot_date >= snapshot.start_date,
            FinancialSnapshots.snapshot_date <= snapshot.end_date,
        )
        .order_by(FinancialSnapshots.snapshot_date)
        .all()
    )

    return {
        "date_range_start": date_range[0],
        "date_range_end": date_range[1],
        "data": [
            {
                "snapshot_date": row.snapshot_date,
                "value": getattr(row, snapshot.metric_type),
            }
            for row in rows
        ],
    }


def refresh_or_create(db: Session, org_id: int):
    _upsert_base(db, org_id)
    _upsert_best(db, org_id)
    _upsert_worst(db, org_id)


def _upsert_base(db: Session, org_id: int):
    now = datetime.now(timezone.utc)
    month, year = now.month, now.year

    monthly_expenses = db.execute(
        text("""
        SELECT NVL(SUM(amount), 0) FROM expenses
        WHERE organization_id = :org_id
        AND EXTRACT(MONTH FROM "date") = :month
        AND EXTRACT(YEAR FROM "date") = :year
    """),
        {"org_id": org_id, "month": month, "year": year},
    ).scalar()

    monthly_revenue = db.execute(
        text("""
        SELECT NVL(SUM(revenue.amount), 0) FROM revenue
        JOIN clients ON clients.id = revenue.client_id
        WHERE clients.organization_id = :org_id
        AND EXTRACT(MONTH FROM revenue.date_received) = :month
        AND EXTRACT(YEAR FROM revenue.date_received) = :year
    """),
        {"org_id": org_id, "month": month, "year": year},
    ).scalar()

    _upsert_snapshot(db, org_id, "Base", monthly_revenue, monthly_expenses)


def _upsert_best(db: Session, org_id: int):
    now = datetime.now(timezone.utc)
    month, year = now.month, now.year

    expected_amounts = db.execute(
        text("""
        SELECT revenue.amount FROM revenue
        JOIN clients ON clients.id = revenue.client_id
        WHERE clients.organization_id = :org_id
        AND EXTRACT(MONTH FROM revenue.date_expected) = :month
        AND EXTRACT(YEAR FROM revenue.date_expected) = :year
    """),
        {"org_id": org_id, "month": month, "year": year},
    ).fetchall()

    non_critical_expenses = db.execute(
        text("""
        SELECT NVL(SUM(amount), 0) FROM expenses
        WHERE organization_id = :org_id
        AND urgency = 'Non-Critical'
        AND EXTRACT(MONTH FROM "date") = :month
        AND EXTRACT(YEAR FROM "date") = :year
    """),
        {"org_id": org_id, "month": month, "year": year},
    ).scalar()

    amounts = [row.amount for row in expected_amounts]
    _upsert_snapshot(db, org_id, "Best", sum(amounts), non_critical_expenses)


def _upsert_worst(db: Session, org_id: int):
    now = datetime.now(timezone.utc)
    month, year = now.month, now.year

    client_revenue = db.execute(
        text("""
        SELECT revenue.amount, clients.reliability_score FROM revenue
        JOIN clients ON clients.id = revenue.client_id
        WHERE clients.organization_id = :org_id
        AND EXTRACT(MONTH FROM revenue.date_expected) = :month
        AND EXTRACT(YEAR FROM revenue.date_expected) = :year
    """),
        {"org_id": org_id, "month": month, "year": year},
    ).fetchall()

    all_expenses = db.execute(
        text("""
        SELECT NVL(SUM(amount), 0) FROM expenses
        WHERE organization_id = :org_id
        AND EXTRACT(MONTH FROM "date") = :month
        AND EXTRACT(YEAR FROM "date") = :year
    """),
        {"org_id": org_id, "month": month, "year": year},
    ).scalar()

    amounts = [row.amount for row in client_revenue]
    scores = [
        row.reliability_score if row.reliability_score is not None else 0
        for row in client_revenue
    ]
    _upsert_snapshot(
        db, org_id, "Worst", calculations.reliable_revenue(amounts, scores), all_expenses
    )


def _upsert_snapshot(
    db: Session, org_id: int, snapshot_type: str, monthly_revenue, monthly_expenses
):
    now = datetime.now(timezone.utc)
    month, year = now.month, now.year

    if snapshot_type == "Base":
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        prev_snapshot = db.execute(
            text("""
            SELECT cash_balance FROM financial_snapshots
            WHERE organization_id = :org_id
            AND EXTRACT(MONTH FROM snapshot_date) = :month
            AND EXTRACT(YEAR FROM snapshot_date) = :year
            AND snapshot_type = 'Base'
        """),
            {"org_id": org_id, "month": prev_month, "year": prev_year},
        ).first()
        prev_balance = prev_snapshot.cash_balance if prev_snapshot else None
        cash_balance = calculations.cash_balance(
            prev_balance, monthly_revenue, monthly_expenses
        )
    else:
        cash_balance = monthly_revenue - monthly_expenses

    snapshot = db.execute(
        text("""
        SELECT * FROM financial_snapshots
        WHERE organization_id = :org_id
        AND EXTRACT(MONTH FROM snapshot_date) = :month
        AND EXTRACT(YEAR FROM snapshot_date) = :year
        AND snapshot_type = :snapshot_type
    """),
        {
            "org_id": org_id,
            "month": month,
            "year": year,
            "snapshot_type": snapshot_type,
        },
    ).first()

    if not snapshot:
        db.execute(
            text("""
            INSERT INTO financial_snapshots
                (organization_id, snapshot_date, snapshot_type, monthly_revenue, monthly_expense, cash_balance)
            VALUES
                (:org_id, :snapshot_date, :snapshot_type, :monthly_revenue, :monthly_expense, :cash_balance)
        """),
            {
                "org_id": org_id,
                "snapshot_date": now.date().replace(day=1),
                "snapshot_type": snapshot_type,
                "monthly_revenue": monthly_revenue,
                "monthly_expense": monthly_expenses,
                "cash_balance": cash_balance,
            },
        )
        logger.info(
            "Created %s snapshot for org %s %s/%s", snapshot_type, org_id, month, year
        )
    else:
        db.execute(
            text("""
            UPDATE financial_snapshots
            SET monthly_revenue = :monthly_revenue,
                monthly_expense = :monthly_expense,
                cash_balance = :cash_balance
            WHERE organization_id = :org_id
            AND EXTRACT(MONTH FROM snapshot_date) = :month
            AND EXTRACT(YEAR FROM snapshot_date) = :year
            AND snapshot_type = :snapshot_type
        """),
            {
                "org_id": org_id,
                "month": month,
                "year": year,
                "snapshot_type": snapshot_type,
                "monthly_revenue": monthly_revenue,
                "monthly_expense": monthly_expenses,
                "cash_balance": cash_balance,
            },
        )
        logger.info(
            "Updated %s snapshot for org %s %s/%s", snapshot_type, org_id, month, year
        )

    db.commit()
