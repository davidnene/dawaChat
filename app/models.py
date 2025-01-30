from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime, timezone
from enum import Enum as pyEnum

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=False)

    admins = relationship(
        "Admin",
        back_populates="hospital",
        cascade="all, delete-orphan",  # Enable cascade delete
        passive_deletes=True
    )
    doctors = relationship(
        "Doctor",
        back_populates="hospital",
        cascade="all, delete-orphan", 
        passive_deletes=True
    )
    
    patients = relationship(
        "Patient",
        back_populates="hospital",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False) 
    hashed_password = Column(String, nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    hospital = relationship("Hospital", back_populates="admins")
    

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    specialty = Column(String)
    role = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    hospital = relationship("Hospital", back_populates="doctors")
    prescriptions = relationship("Prescription", back_populates="doctor")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    hospital = relationship("Hospital")
    prescriptions = relationship("Prescription", back_populates="patient")

class DiseaseTypeEnum(str, pyEnum):
    COMMUNICABLE = "communicable"
    NON_COMMUNICABLE = "non_communicable"

class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    medication = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    observations = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=False)
    diseases_type = Column(Enum(DiseaseTypeEnum, name=("disease_type_enum")))
    treatment_plan = Column(Text, nullable=True)
    doctor_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    doctor = relationship("Doctor")
    patient = relationship("Patient")

class DosageDocument(Base):
    __tablename__ = "dosage_documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("admins.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
