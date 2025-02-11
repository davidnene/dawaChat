from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Prescription, Patient
from schemas import PrescriptionCreate, PrescriptionUpdate, PrescriptionOut
from utils.rbac import verify_role
from utils.asdict import asdict
from db import get_db
from auth import get_current_user
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Create a Prescription (Doctor only for their hospital's patients)
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
    
    return {
            **jsonable_encoder(new_prescription),
            "patient": {
                **jsonable_encoder(new_prescription.patient),
                "hospital": jsonable_encoder(new_prescription.patient.hospital) 
            } if new_prescription.patient else None,
            "doctor": {
                **jsonable_encoder(new_prescription.doctor),
                "hospital": jsonable_encoder(new_prescription.doctor.hospital)  
            } if new_prescription.doctor else None
        }

# Get Prescriptions for a Specific Patient
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
    
    # Serialize the prescriptions, explicitly including hospital info for patient and doctor
    return [
        {
            **jsonable_encoder(pr),
            "patient": {
                **jsonable_encoder(pr.patient),
                "hospital": jsonable_encoder(pr.patient.hospital) 
            } if pr.patient else None,
            "doctor": {
                **jsonable_encoder(pr.doctor),
                "hospital": jsonable_encoder(pr.doctor.hospital)  
            } if pr.doctor else None
        }
        for pr in prescriptions
    ]

# Update a Prescription
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
    existing_prescription.observations = prescription.observations or existing_prescription.observations
    existing_prescription.diagnosis = prescription.diagnosis or existing_prescription.diagnosis
    existing_prescription.diseases_type = prescription.diseases_type or existing_prescription.diseases_type
    existing_prescription.treatment_plan = prescription.treatment_plan or existing_prescription.treatment_plan
    existing_prescription.doctor_notes = prescription.doctor_notes or existing_prescription.doctor_notes

    db.commit()
    db.refresh(existing_prescription)
    
    return {
            **jsonable_encoder(existing_prescription),
            "patient": {
                **jsonable_encoder(existing_prescription.patient),
                "hospital": jsonable_encoder(existing_prescription.patient.hospital) 
            } if existing_prescription.patient else None,
            "doctor": {
                **jsonable_encoder(existing_prescription.doctor),
                "hospital": jsonable_encoder(existing_prescription.doctor.hospital)  
            } if existing_prescription.doctor else None
        }

# Delete a Prescription
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
