from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum 

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
    role: str


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(AdminBase):
    """Schema for updating admin details."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    password: Optional[str] = None


class Admin(AdminBase):
    id: int
    hospital_id: int
    hospital: Hospital

    class Config:
        orm_mode = True


class AdminOut(AdminBase):
    id: int
    hospital_name: str

    class Config:
        orm_mode = True


# Doctor Schemas
class DoctorBase(BaseModel):
    name: str
    email: EmailStr
    specialty: str


class DoctorCreate(DoctorBase):
    password: str
    role: str


class DoctorUpdate(DoctorBase):
    """Schema for updating doctor details."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    specialty: Optional[str] = None
    password: Optional[str] = None

class DoctorOut(DoctorBase):
    id: int

    class Config:
        orm_mode = True

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

class PatientOut(PatientBase):
    id: int

    class Config:
        orm_mode = True
        
class Patient(PatientBase):
    id: int
    hospital_id: int
    hospital: Hospital  # Hospital that the patient belongs to
    prescriptions: List["Prescription"] = []  # Prescriptions linked to the patient

    class Config:
        orm_mode = True


# Enum for disease type
class DiseaseTypeEnum(str, Enum):
    COMMUNICABLE = "communicable"
    NON_COMMUNICABLE = "non_communicable"

# Base schema for Prescription
class PrescriptionBase(BaseModel):
    medication: str
    dosage: str
    observations: Optional[str] = None
    diagnosis: str
    diseases_type: DiseaseTypeEnum
    treatment_plan: Optional[str] = None
    doctor_notes: Optional[str] = None

# Schema for creating a prescription
class PrescriptionCreate(PrescriptionBase):
    pass

# Schema for updating a prescription
class PrescriptionUpdate(BaseModel):
    medication: Optional[str] = None
    dosage: Optional[str] = None
    observations: Optional[str] = None
    diagnosis: Optional[str] = None
    diseases_type: Optional[DiseaseTypeEnum] = None
    treatment_plan: Optional[str] = None

# Schema for response output
class PrescriptionOut(PrescriptionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Prescription(PrescriptionBase):
    id: int
    patient_id: int
    patient: Patient
    doctor_id: int
    doctor: Doctor
    
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
