"""Business logic for Clients"""

from sqlalchemy.orm import Session
from models import Clients
import schema
from logger import get_logger

logger = get_logger(__name__)


def add_client(client: schema.ClientsCreate, db: Session):
    try:
        new_client = Clients(
            organization_id=client.organization_id,
            name=client.name,
            email=client.email,
            contact_number=client.contact_number,
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        logger.info("Client %s added to org %s", client.name, client.organization_id)
        return new_client
    except Exception:
        db.rollback()
        raise

def update_reliability_score(db: Session, client_id: int):
    score = recalculate_reliability(db, client_id)
    db.execute(
        text("""
        UPDATE clients SET reliability_score = :score
        WHERE id = :client_id
    """),
        {"score": score, "client_id": client_id},
    )
    db.commit()


MAX_DAYS_LATE = 90


def recalculate_reliability(db: Session, client_id: int) -> int:
    rows = db.execute(
        text("""
        SELECT GREATEST(0, CAST(date_received - date_expected AS NUMBER)) AS days_late
        FROM revenue
        WHERE client_id = :client_id
        AND date_received IS NOT NULL
    """),
        {"client_id": client_id},
    ).fetchall()

    if not rows:
        return 100  # no payment history, benefit of the doubt

    contributions = [max(0.0, 1 - (row.days_late / MAX_DAYS_LATE)) for row in rows]
    score = round(sum(contributions) / len(contributions) * 100)
    return min(score, 100)