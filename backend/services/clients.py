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

