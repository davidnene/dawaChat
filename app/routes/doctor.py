from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Prescription, Patient
from schemas import PrescriptionCreate, PrescriptionUpdate, PrescriptionOut
from utils.rbac import verify_role
from db import get_db
from auth import get_current_user
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 1. Create a Prescription (Doctor only for their hospital's patients)
@router.post("/api/create-prescription/", response_model=PrescriptionOut, status_code=status.HTTP_201_CREATED)
async def create_prescription(
    prescription: PrescriptionCreate,
    patient_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "doctor")
    
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.hospital_id == current_user.hospital_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found or does not belong to your hospital")
    
    new_prescription = Prescription(
    doctor_id=current_user.id,
    patient_id=patient.id,
    medication=prescription.medication,
    dosage=prescription.dosage,
    observations=prescription.observations,
    diagnosis=prescription.diagnosis,
    diseases_type=prescription.diseases_type,
    treatment_plan=prescription.treatment_plan,
    doctor_notes=prescription.doctor_notes
    )

    db.add(new_prescription)
    db.commit()
    db.refresh(new_prescription)
    
    return new_prescription

# 2. Get Prescriptions for a Specific Patient
@router.get("/api/prescriptions/{patient_id}", response_model=List[PrescriptionOut])
async def get_prescriptions(
    patient_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "doctor")
    
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.hospital_id == current_user.hospital_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found or does not belong to your hospital")
    
    prescriptions = db.query(Prescription).filter(Prescription.patient_id == patient_id).all()
    return prescriptions

# 3. Update a Prescription
@router.put("/api/update-prescription/{prescription_id}", response_model=PrescriptionOut)
async def update_prescription(
    prescription_id: int,
    prescription: PrescriptionUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "doctor")
    
    existing_prescription = db.query(Prescription).filter(Prescription.id == prescription_id, Prescription.doctor_id == current_user.id).first()
    if not existing_prescription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found or does not belong to you")
    
    existing_prescription.medication = prescription.medication or existing_prescription.medication
    existing_prescription.dosage = prescription.dosage or existing_prescription.dosage
    existing_prescription.instructions = prescription.instructions or existing_prescription.instructions
    db.commit()
    db.refresh(existing_prescription)
    
    return existing_prescription

# 4. Delete a Prescription
@router.delete("/api/delete-prescription/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prescription(
    prescription_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "doctor")
    
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id, Prescription.doctor_id == current_user.id).first()
    if not prescription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found or does not belong to you")
    
    db.delete(prescription)
    db.commit()
    return {"detail": "Prescription deleted successfully"}
