"""Business logic for Predictive Analysis"""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from models import Revenue, Expenses, Clients, FinancialSnapshots
from logger import get_logger

logger = get_logger(__name__)

def calculate_best(db, org_id):
    # TODO: get projected figures from prediction_service
    pass


def calculate_worst(db, org_id):
    # TODO: get projected figures from prediction_service
    pass