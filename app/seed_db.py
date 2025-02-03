from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import Patient, Prescription, Doctor, Admin, Hospital, DiseaseTypeEnum
from db import SessionLocal, engine, Base
from auth import get_password_hash
from dotenv import load_dotenv

load_dotenv(override=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()

    # Check if the database is already seeded
    if db.query(Hospital).count() > 0:
        print("Database already seeded")
        db.close()
        return

    # Create hospitals
    hospital1 = Hospital(name="Admin Hospital Hold", location="Nairobi")
    hospital2 = Hospital(name="Kenyatta National Hospital", location="Nairobi")

    db.add_all([hospital1, hospital2])
    db.commit()

    # Create the super admin
    super_admin = Admin(
        name="Super Admin",
        email="superadmin@dawachat.ai",
        hashed_password=get_password_hash("SuperAdminPassword1"),
        role="super_admin",
        hospital_id=hospital1.id
    )

    # Create admins
    admin1 = Admin(
        name="Admin John Doe",
        email="admin1@dawachat.ai",
        hashed_password=get_password_hash("AdminPassword1"),
        role="admin",
        hospital_id=hospital1.id
    )
    admin2 = Admin(
        name="Admin Jane Smith",
        email="admin2@dawachat.ai",
        hashed_password=get_password_hash("AdminPassword2"),
        role="admin",
        hospital_id=hospital2.id
    )

    # Create doctors
    doctor1 = Doctor(
        name="Dr. Rose Ochieng",
        email="rose@dawachat.ai",
        role="doctor",
        specialty="Gynecology",
        hashed_password=get_password_hash("doctorpassword1"),
        hospital_id=hospital1.id
    )
    doctor2 = Doctor(
        name="Dr. Idris Omollo",
        email="idris@dawachat.ai",
        role="doctor",
        specialty="Clinician",
        hashed_password=get_password_hash("doctorpassword2"),
        hospital_id=hospital2.id
    )
    doctor3 = Doctor(
        name="Dr. Enock Omwami",
        email="enock@dawachat.ai",
        role="doctor",
        specialty="Nurse",
        hashed_password=get_password_hash("doctorpassword3"),
        hospital_id=hospital1.id
    )

    db.add_all([super_admin, admin1, admin2, doctor1, doctor2, doctor3])
    db.commit()

    # Create patients
    patients = [
        Patient(name="Alice Johnson", email="alice@example.com", hospital_id=hospital1.id),
        Patient(name="Bob Smith", email="bob@example.com", hospital_id=hospital1.id),
        Patient(name="Charlie Davis", email="charlie@example.com", hospital_id=hospital2.id),
    ]

    db.add_all(patients)
    db.commit()

    # Retrieve patient IDs
    alice = db.query(Patient).filter_by(email="alice@example.com").first()
    bob = db.query(Patient).filter_by(email="bob@example.com").first()
    charlie = db.query(Patient).filter_by(email="charlie@example.com").first()

    # Create prescriptions with doctor_notes
    prescriptions = [
        Prescription(
            patient_id=alice.id,
            doctor_id=doctor1.id,
            medication="Amoxicillin 500mg",
            dosage="1 capsule, 3 times a day",
            observations="Patient shows signs of mild fever and coughing.",
            diagnosis="Acute bacterial infection",
            diseases_type=DiseaseTypeEnum.COMMUNICABLE,
            treatment_plan="Continue for 7 days, follow-up in 3 days.",
            doctor_notes="Monitor for signs of allergic reactions. May cause mild diarrhea.",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        Prescription(
            patient_id=bob.id,
            doctor_id=doctor2.id,
            medication="Metformin 850mg",
            dosage="1 tablet, twice a day",
            observations="Patient has high blood sugar levels.",
            diagnosis="Type 2 Diabetes",
            diseases_type=DiseaseTypeEnum.NON_COMMUNICABLE,
            treatment_plan="Maintain a healthy diet and take medication as prescribed.",
            doctor_notes="Watch for signs of low blood sugar. Possible side effects: nausea and stomach upset.",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        Prescription(
            patient_id=charlie.id,
            doctor_id=doctor3.id,
            medication="Ibuprofen 400mg",
            dosage="1 tablet, every 6 hours as needed",
            observations="Complaints of muscle pain after an injury.",
            diagnosis="Muscle strain",
            diseases_type=DiseaseTypeEnum.NON_COMMUNICABLE,
            treatment_plan="Rest, apply ice packs, and take medication as needed.",
            doctor_notes="Avoid alcohol. May cause stomach irritation if taken without food.",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
    ]

    db.add_all(prescriptions)
    db.commit()

    db.close()
    print("Database seeded with super_admin, admins, hospitals, doctors, patients, and prescriptions.")

if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    Base.metadata.create_all(bind=engine)  # Recreate tables
    seed_database()
