# In your route (super_admin.py or any relevant file)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Hospital, Admin
from schemas import HospitalCreate, AdminCreate, HospitalOut, AdminOut
from utils.rbac import verify_role
from db import get_db
from auth import get_current_user
from fastapi.security import OAuth2PasswordBearer
from auth import get_password_hash

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Route for creating a hospital
@router.post("/api/create-hospital/", response_model=HospitalOut, status_code=status.HTTP_201_CREATED)
async def create_hospital(
    hospital: HospitalCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Verify if the current user is a super admin
    current_user = get_current_user(token, db)
    verify_role(current_user, "super_admin")

    # Check if hospital name already exists
    if db.query(Hospital).filter(Hospital.name == hospital.name).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Hospital name already exists")

    # Create the new hospital
    new_hospital = Hospital(name=hospital.name, location=hospital.location)
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)

    # Return the hospital data using Pydantic model
    return HospitalOut(id=new_hospital.id, name=new_hospital.name, location=new_hospital.location)


# Route for creating an admin
@router.post("/api/create-admin/", response_model=AdminOut, status_code=status.HTTP_201_CREATED)
async def create_admin(
    admin: AdminCreate,
    hospital_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Verify if the current user is a super admin
    current_user = get_current_user(token, db)
    verify_role(current_user, "super_admin")

    # Check if the hospital exists
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    # Check if the admin email already exists
    if db.query(Admin).filter(Admin.email == admin.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin email already exists")

    # Hash the password
    hashed_password = get_password_hash(admin.password)
    new_admin = Admin(
        name=admin.name,
        email=admin.email,
        hashed_password=hashed_password,
        hospital_id=hospital.id
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    # Return the admin data using Pydantic model
    return AdminOut(id=new_admin.id, name=new_admin.name, email=new_admin.email)
