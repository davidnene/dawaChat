from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from models import Doctor
from sqlalchemy.orm import Session

SECRET_KEY = "aiplanettask1234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(email: str, password: str, db_session):
    doctor = db_session.query(Doctor).filter(Doctor.email == email).first()
    if doctor and verify_password(password, doctor.hashed_password):
        return doctor
    return None


def get_current_user(token: str , db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Use your secret key
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(Doctor).filter(Doctor.email == email).first()  # Fetch user from DB
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user

