from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Doctor, Patient, Admin
from schemas import DoctorCreate, DoctorUpdate, PatientCreate, PatientUpdate, DoctorOut, PatientOut
from utils.rbac import verify_role
from db import get_db
from auth import get_current_user
from fastapi.security import OAuth2PasswordBearer
from auth import get_password_hash

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 1. Create a Doctor (Admin only for their hospital)
@router.post("/api/create-doctor/", response_model=DoctorOut, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    doctor: DoctorCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "admin")
    
    hashed_password = get_password_hash(doctor.password)
    new_doctor = Doctor(
        name=doctor.name,
        email=doctor.email,
        role=doctor.role,
        specialty=doctor.specialty,
        hospital_id=current_user.hospital_id,
        hashed_password=hashed_password
    )
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    
    return DoctorOut(id=new_doctor.id, name=new_doctor.name, email=new_doctor.email, specialty=new_doctor.specialty)

# 2. List Doctors in Admin's Hospital
@router.get("/api/doctors/", response_model=List[DoctorOut])
async def get_doctors(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "admin")
    
    doctors = db.query(Doctor).filter(Doctor.hospital_id == current_user.hospital_id).all()
    return [DoctorOut(id=d.id, name=d.name, email=d.email, specialty=d.specialty) for d in doctors]

# 3. Update a Doctor (Admin only for their hospital)
@router.put("/api/update-doctor/{doctor_id}", response_model=DoctorOut)
async def update_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "admin")
    
    existing_doctor = db.query(Doctor).filter(Doctor.id == doctor_id, Doctor.hospital_id == current_user.hospital_id).first()
    if not existing_doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    
    existing_doctor.name = doctor.name or existing_doctor.name
    existing_doctor.email = doctor.email or existing_doctor.email
    existing_doctor.specialty = doctor.specialty or existing_doctor.specialty
    if doctor.password:
        existing_doctor.password_hash = get_password_hash(doctor.password)
    db.commit()
    db.refresh(existing_doctor)
    
    return DoctorOut(id=existing_doctor.id, name=existing_doctor.name, email=existing_doctor.email, specialty=existing_doctor.specialty)

# 4. Delete a Doctor (Admin only for their hospital)
@router.delete("/api/delete-doctor/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    doctor_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "admin")
    
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id, Doctor.hospital_id == current_user.hospital_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    
    db.delete(doctor)
    db.commit()
    return {"detail": "Doctor deleted successfully"}


# 5. Create a Patient (Admin only for their hospital)
@router.post("/api/create-patient/", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient: PatientCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "admin")
    
    new_patient = Patient(
        name=patient.name,
        email=patient.email,
        age=patient.age,
        hospital_id=current_user.hospital_id
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    
    return PatientOut(id=new_patient.id, name=new_patient.name, email=new_patient.email, age=new_patient.age)


# 6. List Patients in Admin's Hospital
@router.get("/api/patients/", response_model=List[PatientOut])
async def get_patients(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "admin")
    
    patients = db.query(Patient).filter(Patient.hospital_id == current_user.hospital_id).all()
    return [PatientOut(id=p.id, name=p.name, email=p.email, age=p.age) for p in patients]


# 7. Update a Patient (Admin only for their hospital)
@router.put("/api/update-patient/{patient_id}", response_model=PatientOut)
async def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "admin")
    
    existing_patient = db.query(Patient).filter(Patient.id == patient_id, Patient.hospital_id == current_user.hospital_id).first()
    if not existing_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    existing_patient.name = patient.name or existing_patient.name
    existing_patient.email = patient.email or existing_patient.email
    existing_patient.age = patient.age or existing_patient.age
    db.commit()
    db.refresh(existing_patient)
    
    return PatientOut(id=existing_patient.id, name=existing_patient.name, email=existing_patient.email, age=existing_patient.age)


# 8. Delete a Patient (Admin only for their hospital)
@router.delete("/api/delete-patient/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "admin")
    
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.hospital_id == current_user.hospital_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    return {"detail": "Patient deleted successfully"}
