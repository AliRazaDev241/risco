"""Business logic for Revenue"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Revenue
import schema
from logger import get_logger
logger = get_logger(__name__)

def add_revenue(revenue: schema.RevenueCreate, db: Session):
    client_row = db.execute(
        text("SELECT id FROM clients WHERE name = :name"),
        {"name": revenue.client_name}
    ).fetchone()
    if not client_row:
        raise LookupError(f"No client found with name {revenue.client_name}")

    try:
        new_revenue = Revenue(
            client_id=client_row.id,
            revenue_type=revenue.revenue_type,
            date_expected=revenue.date_expected,
            date_received=revenue.date_received,
            amount=revenue.amount,
        )
        db.add(new_revenue)
        db.commit()
        db.refresh(new_revenue)
        logger.info("Revenue added for client %s", revenue.client_name)
        return new_revenue
    except Exception as e:
        db.rollback()
        raise
    
def list_five_revenue(org_id: int, revenue_type: str, page_no: int, db: Session):
    org = db.execute(text("SELECT id FROM organizations WHERE id = :org_id"), {"org_id": org_id}).fetchone()
    if not org:
        raise LookupError(f"No organization found with id {org_id}")

    params = {"org_id": org_id, "revenue_type": revenue_type}

    count = db.execute(text("""
        SELECT COUNT(*) FROM revenue
        JOIN clients ON clients.id = revenue.client_id
        WHERE clients.organization_id = :org_id
        AND revenue.revenue_type = :revenue_type
    """), params).scalar()

    total_pages = max(1, -(-count // 5))  # ceiling division

    offset = (page_no - 1) * 5
    rows = db.execute(text("""
        SELECT clients.name AS client_name, clients.email AS client_email,
               revenue.date_expected, revenue.date_received, revenue.amount
        FROM revenue
        JOIN clients ON clients.id = revenue.client_id
        JOIN organizations ON organizations.id = clients.organization_id
        WHERE organizations.id = :org_id
        AND revenue.revenue_type = :revenue_type
        ORDER BY revenue.date_expected ASC, revenue.id ASC
        OFFSET :offset ROWS FETCH NEXT 5 ROWS ONLY
    """), {**params, "offset": offset}).fetchall()

    return {"items": rows, "total_pages": total_pages, "current_page": page_no}