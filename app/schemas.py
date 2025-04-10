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
        from_attributes = True

class Hospital(HospitalOut):
    admins: List["AdminOut"] = []  
    doctors: List["DoctorOut"] = []

    class Config:
        from_attributes = True

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

class AdminOut(AdminBase):
    id: int
    hospital: Optional[HospitalOut]  # Nested hospital details

    class Config:
        from_attributes = True

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
    hospital: Optional[HospitalOut]  # Nested hospital details
    prescriptions: List["PrescriptionOut"] = []  # List of prescriptions

    class Config:
        from_attributes = True

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
    hospital: Optional[HospitalOut]  # Nested hospital details
    prescriptions: List["PrescriptionOut"] = []  # List of prescriptions

    class Config:
        from_attributes = True

# Enum for disease type
class DiseaseTypeEnum(str, Enum):
    COMMUNICABLE = "communicable"
    NON_COMMUNICABLE = "non_communicable"

# Prescription Schemas
class PrescriptionBase(BaseModel):
    medication: str
    dosage: str
    observations: Optional[str] = None
    diagnosis: str
    diseases_type: DiseaseTypeEnum
    treatment_plan: Optional[str] = None
    doctor_notes: Optional[str] = None

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(BaseModel):
    medication: Optional[str] = None
    dosage: Optional[str] = None
    doctor_notes: Optional[str] = None
    observations: Optional[str] = None
    diagnosis: Optional[str] = None
    diseases_type: Optional[DiseaseTypeEnum] = None
    treatment_plan: Optional[str] = None

class PrescriptionOut(PrescriptionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    patient: Optional[PatientOut]  # Nested patient details
    doctor: Optional[DoctorOut]  # Nested doctor details

    class Config:
        from_attributes = True

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

class DosageDocumentOut(DosageDocumentBase):
    id: int
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

# User-related schemas (for login)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class QueryDosageRequest(BaseModel):
    query: str
    
class EmpaticaDataIn(BaseModel):
    x: float 
    y: float 
    z: float 
    eda: float 
    hr: float 
    temp: float 
    time_of_day: str 
    day_of_week: str 
