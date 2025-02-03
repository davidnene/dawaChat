from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Hospital, Admin
from schemas import HospitalCreate, HospitalUpdate, AdminCreate, AdminUpdate, HospitalOut, AdminOut
from utils.rbac import verify_role
from db import get_db
from auth import get_current_user
from fastapi.security import OAuth2PasswordBearer
from auth import get_password_hash

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 1. Create a Hospital
@router.post("/api/create-hospital/", response_model=HospitalOut, status_code=status.HTTP_201_CREATED)
async def create_hospital(
    hospital: HospitalCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "super_admin")

    if db.query(Hospital).filter(Hospital.name == hospital.name).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Hospital name already exists")

    new_hospital = Hospital(name=hospital.name, location=hospital.location)
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)

    return HospitalOut(id=new_hospital.id, name=new_hospital.name, location=new_hospital.location)


# 2. List All Hospitals
@router.get("/api/hospitals/", response_model=List[HospitalOut])
async def get_hospitals(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "super_admin")

    hospitals = db.query(Hospital).all()
    return [HospitalOut(id=hospital.id, name=hospital.name, location=hospital.location) for hospital in hospitals]


# 3. Update a Hospital
@router.put("/api/update-hospital/{hospital_id}", response_model=HospitalOut)
async def update_hospital(
    hospital_id: int,
    hospital: HospitalUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "super_admin")

    existing_hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not existing_hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    existing_hospital.name = hospital.name or existing_hospital.name
    existing_hospital.location = hospital.location or existing_hospital.location
    db.commit()
    db.refresh(existing_hospital)

    return HospitalOut(id=existing_hospital.id, name=existing_hospital.name, location=existing_hospital.location)


# 4. Delete a Hospital
@router.delete("/api/delete-hospital/{hospital_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hospital(
    hospital_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "super_admin")

    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    db.delete(hospital)
    db.commit()
    return {"detail": "Hospital deleted successfully"}


# 5. Create an Admin
@router.post("/api/create-admin/", response_model=AdminOut, status_code=status.HTTP_201_CREATED)
async def create_admin(
    admin: AdminCreate,
    hospital_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db, role="super_admin")
    verify_role(current_user, "super_admin")

    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    if db.query(Admin).filter(Admin.email == admin.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin email already exists")

    hashed_password = get_password_hash(admin.password)
    new_admin = Admin(
        name=admin.name,
        email=admin.email,
        role=admin.role,
        hashed_password=hashed_password,
        hospital_id=hospital.id
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return AdminOut(id=new_admin.id, name=new_admin.name, email=new_admin.email, role=new_admin.role, hospital_name=new_admin.hospital.name)


# 6. List All Admins
@router.get("/api/admins/", response_model=List[AdminOut])
async def get_admins(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "super_admin")

    admins = db.query(Admin).all()
    return [AdminOut(id=admin.id, name=admin.name, email=admin.email, role=admin.role, hospital_name=admin.hospital.name) for admin in admins]


# 7. Update an Admin
@router.put("/api/update-admin/{admin_id}", response_model=AdminOut)
async def update_admin(
    admin_id: int,
    admin: AdminUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "super_admin")

    existing_admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not existing_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    existing_admin.name = admin.name or existing_admin.name
    existing_admin.email = admin.email or existing_admin.email
    if admin.password:
        existing_admin.hashed_password = get_password_hash(admin.password)
    db.commit()
    db.refresh(existing_admin)

    return AdminOut(id=existing_admin.id, name=existing_admin.name, email=existing_admin.email, role=existing_admin.role,hospital_name=existing_admin.hospital.name)


# 8. Delete an Admin
@router.delete("/api/delete-admin/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin(
    admin_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "super_admin")

    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    db.delete(admin)
    db.commit()
    return {"detail": "Admin deleted successfully"}
