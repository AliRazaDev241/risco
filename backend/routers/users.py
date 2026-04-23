from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
import schema, models 

router = APIRouter(prefix="/users", tags=["Users"])

#@router.get 