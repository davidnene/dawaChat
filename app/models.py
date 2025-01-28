from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    admins = relationship("Admin", back_populates="hospital")
    doctors = relationship("Doctor", back_populates="hospital")

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False) 
    hashed_password = Column(String, nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    hospital = relationship("Hospital", back_populates="admins")
    

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    hospital = relationship("Hospital", back_populates="doctors")
    prescriptions = relationship("Prescription", back_populates="doctor")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    hospital = relationship("Hospital")
    prescriptions = relationship("Prescription", back_populates="patient")

class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    medication = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")

class DosageDocument(Base):
    __tablename__ = "dosage_documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("admins.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
