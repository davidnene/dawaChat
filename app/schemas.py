from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Hospital Schemas
class HospitalBase(BaseModel):
    name: str
    location: str


class HospitalCreate(HospitalBase):
    pass


class HospitalUpdate(HospitalBase):
    """Schema for updating hospital details."""
    name: Optional[str] = None
    location: Optional[str] = None


class HospitalOut(HospitalBase):
    id: int

    class Config:
        orm_mode = True


class Hospital(HospitalBase):
    id: int
    admins: List["Admin"] = []  # List of admins for this hospital
    doctors: List["Doctor"] = []  # List of doctors for this hospital

    class Config:
        orm_mode = True


# Admin Schemas
class AdminBase(BaseModel):
    name: str
    email: EmailStr


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(AdminBase):
    """Schema for updating admin details."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class Admin(AdminBase):
    id: int
    hospital_id: int
    hospital: Hospital  # This will include the hospital's details

    class Config:
        orm_mode = True


class AdminOut(AdminBase):
    id: int

    class Config:
        orm_mode = True


# Doctor Schemas
class DoctorBase(BaseModel):
    name: str
    email: EmailStr


class DoctorCreate(DoctorBase):
    password: str


class DoctorUpdate(DoctorBase):
    """Schema for updating doctor details."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class Doctor(DoctorBase):
    id: int
    hospital_id: int
    hospital: Hospital 
    prescriptions: List["Prescription"] = []  # Prescriptions linked to the doctor

    class Config:
        orm_mode = True


# Patient Schemas
class PatientBase(BaseModel):
    name: str
    email: EmailStr


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    """Schema for updating patient details."""
    name: Optional[str] = None 
    email: Optional[EmailStr] = None


class Patient(PatientBase):
    id: int
    hospital_id: int
    hospital: Hospital  # Hospital that the patient belongs to
    prescriptions: List["Prescription"] = []  # Prescriptions linked to the patient

    class Config:
        orm_mode = True


# Prescription Schemas
class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    medication: str
    dosage: str
    frequency: str
    notes: Optional[str] = None


class PrescriptionCreate(PrescriptionBase):
    pass


class PrescriptionUpdate(PrescriptionBase):
    """Schema for updating prescription details."""
    medication: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    notes: Optional[str] = None


class Prescription(PrescriptionBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


# Dosage Document Schemas
class DosageDocumentBase(BaseModel):
    title: str
    content: str


class DosageDocumentCreate(DosageDocumentBase):
    pass


class DosageDocumentUpdate(DosageDocumentBase):
    """Schema for updating dosage document details."""
    title: Optional[str] = None
    content: Optional[str] = None


class DosageDocument(DosageDocumentBase):
    id: int
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        orm_mode = True


# User-related schemas (for login)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class QueryDosageRequest(BaseModel):
    query: str
