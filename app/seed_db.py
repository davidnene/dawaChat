# seed_db.py
from models import Doctor
from db import SessionLocal, engine, Base
from auth import get_password_hash
from dotenv import load_dotenv

load_dotenv()

# Create the database tables
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()

    # Check if the database is already seeded
    if db.query(Doctor).count() > 0:
        print("Database already seeded")
        db.close()
        return

    # Create the super admin
    super_admin = Doctor(
        name="Super Admin",
        email="admin@dawachat.ai",
        hashed_password=get_password_hash("Qwerty1."),
        role="super_admin"
    )

    # Create doctors
    doctor1 = Doctor(
        name="Dr. Rose Ochieng",
        email="rose@dawachat.ai",
        hashed_password=get_password_hash("doctorpassword"),
        role="doctor"
    )
    doctor2 = Doctor(
        name="Dr. Idris Omollo",
        email="idris@dawachat.ai",
        hashed_password=get_password_hash("doctorpassword"),
        role="doctor"
    )
    doctor3 = Doctor(
        name="Dr. Enock Omwami",
        email="enock.dawachat.ai",
        hashed_password=get_password_hash("doctorpassword"),
        role="doctor"
    )

    # Add to the session and commit
    db.add_all([super_admin, doctor1, doctor2, doctor3])
    db.commit()
    db.close()
    print("Database seeded with super admin and doctors.")

if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_database()
