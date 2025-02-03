from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from models import Doctor, Admin
from sqlalchemy.orm import Session
from typing import Union

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

def authenticate_user(email: str, password: str, db_session: Session):
    # Check if the user exists in any role (Doctor, Admin, etc.)
    user = db_session.query(Doctor).filter(Doctor.email == email).first()
    if not user:
        user = db_session.query(Admin).filter(Admin.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def get_current_user(token: str, db: Session, role: Union[str, None] = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # Checking if the user exists in multiple roles (Doctor, Admin, etc.)
        user = db.query(Doctor).filter(Doctor.email == email).first() or db.query(Admin).filter(Admin.email == email).first()
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # If a role is specified, check that the user's role matches
    if role and user.role != role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized as {role}",
        )
    
    return user
