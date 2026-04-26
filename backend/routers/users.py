"""API endpoints for Users"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema
from services import users as user_service
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schema.UserResponse)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    existing = user_service.get_user_by_email(user.email, db)
    if existing:
        logger.warning("Registration attempt with existing email: %s", user.email)
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(user, db)


@router.post("/login", response_model=schema.UserResponse)
def login(credentials: schema.UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(credentials.email, credentials.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user
