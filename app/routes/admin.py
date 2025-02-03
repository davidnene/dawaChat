from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from models import Doctor, Patient, Admin, Hospital, Prescription
from schemas import DoctorCreate, DoctorUpdate, PatientCreate, PatientUpdate, PatientOut
from utils.rbac import verify_role
from utils.asdict import asdict
from db import get_db
from auth import get_current_user
from fastapi.security import OAuth2PasswordBearer
from auth import get_password_hash
from sqlalchemy.inspection import inspect

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Create a Doctor (Admin only for their hospital)
@router.post("/api/create-doctor/", status_code=status.HTTP_201_CREATED)
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
    
    return {
        **asdict(new_doctor),
        "hospital": asdict(new_doctor.hospital) if new_doctor.hospital else None
    }

# List Doctors in Admin's Hospital
@router.get("/api/doctors/")
async def get_doctors(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "admin")
    
    doctors = (
        db.query(Doctor)
        .options(joinedload(Doctor.hospital))
        .filter(Doctor.hospital_id == current_user.hospital_id)
        .all()
    )
    
    return [
        {
            "id": d.id,
            "name": d.name,
            "email": d.email,
            "specialty": d.specialty,
            "hospital": asdict(d.hospital) if d.hospital else None
        }
        for d in doctors
    ]

# Update a Doctor
@router.put("/api/update-doctor/{doctor_id}")
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
    
    return {
        **asdict(existing_doctor),
        "hospital": asdict(existing_doctor.hospital) if existing_doctor.hospital else None
    }

# Delete a Doctor (Admin only for their hospital)
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

# Create a Patient (Admin only for their hospital)
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
        hospital_id=current_user.hospital_id
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    
    return {
            **asdict(new_patient),
            "hospital": asdict(new_patient.hospital) if new_patient.hospital else None,
            # "prescriptions": [asdict(pr) for pr in p.prescriptions] if p.prescriptions and current_user.role=="doctor" else []
        }

# List Patients with Prescriptions
@router.get("/api/patients/")
async def get_patients(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    if current_user.role == "admin" or current_user.role == "doctor":
        pass
    else:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required role: Admin or Doctor",
        )

    patients = (
        db.query(Patient)
        .options(joinedload(Patient.hospital), joinedload(Patient.prescriptions))
        .filter(Patient.hospital_id == current_user.hospital_id)
        .all()
    )

    return [
        {
            **asdict(p),
            "hospital": asdict(p.hospital) if p.hospital else None,
            "prescriptions": [asdict(pr) for pr in p.prescriptions] if p.prescriptions and current_user.role=="doctor" else []
        }
        for p in patients
    ]

# Update a Patient
@router.put("/api/update-patient/{patient_id}")
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
    db.commit()
    db.refresh(existing_patient)
    
    return {
        **asdict(existing_patient),
        "hospital": asdict(existing_patient.hospital) if existing_patient.hospital else None,
        "prescriptions": [asdict(pr) for pr in existing_patient.prescriptions] if existing_patient.prescriptions and current_user.role=="doctor" else []
    }

#Delete a Patient (Admin only for their hospital)
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