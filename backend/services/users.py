""" Business logic for Users """
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import Users
import schema
from logger import get_logger

logger = get_logger(__name__)

# Store Password to be encrypted
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    "Hashes password using bcrypt for security before storing"
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    "Verfies user for login"
    return pwd_context.verify(plain, hashed)

def get_user_by_id(user_id: int, db: Session):
    "Fetches user details using id"
    return db.query(Users).filter(Users.id == user_id).first()

def get_user_by_email(email: str, db: Session):
    "fetches user details using email"
    return db.query(Users).filter(Users.email == email).first()

def create_user(user: schema.UserCreate, db: Session):
    "Creates a new user within the database"
    try:
        new_user = Users(
            email=user.email,
            password_hash=hash_password(user.password),
            first_name=user.first_name,
            last_name=user.last_name
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info("User created: %s", new_user.email)
        return new_user
    except Exception as e:
        db.rollback()
        logger.error("Failed to create user: %s", e)
        raise

def authenticate_user(email: str, password: str, db: Session):
    " Validates user identity "
    user = get_user_by_email(email, db)
    if not user:
        logger.warning("Login failed - email not found: %s", email)
        return None
    if not verify_password(password, user.password_hash):
        logger.warning("Login failed - wrong password for: %s", email)
        return None
    logger.info("User authenticated: %s", email)
    return user
