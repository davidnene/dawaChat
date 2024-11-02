from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from db import Base

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="doctor")  # Set "super_admin" for super admin users

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    medication = Column(String)
    dosage = Column(String)
    frequency = Column(String)
    notes = Column(String)
    timestamp = Column(DateTime)

    patient = relationship("Patient")
    doctor = relationship("Doctor")

class DosageDocument(Base):
    __tablename__ = "dosage_documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)  # Store extracted text for querying
    uploaded_by = Column(Integer, ForeignKey("doctors.id"))

    uploader = relationship("Doctor")
