from models import Doctor, Admin, Hospital
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

    # Create the super admin
    super_admin = Admin(
        name="Super Admin",
        email="superadmin@dawachat.ai",
        hashed_password=get_password_hash("SuperAdminPassword1"),
        role="super_admin",
        hospital_id=1
        
    )
    
    # Create hospitals
    hospital1 = Hospital(
        name="Admin Hospital Hold",
        location="Nairobi",
        # contact="0712345678",
    )
    hospital2 = Hospital(
        name="Kenyatta National Hospital",
        location="Nairobi",
        # contact="0723456789",
    )

    # Create admins
    admin1 = Admin(
        name="Admin John Doe",
        email="admin1@dawachat.ai",
        hashed_password=get_password_hash("AdminPassword1"),
        role="admin",
        hospital_id=1,  # Assigning hospital1
    )
    admin2 = Admin(
        name="Admin Jane Smith",
        email="admin2@dawachat.ai",
        hashed_password=get_password_hash("AdminPassword2"),
        role="admin",
        hospital_id=2,  # Assigning hospital2
    )

    # Create doctors
    doctor1 = Doctor(
        name="Dr. Rose Ochieng",
        email="rose@dawachat.ai",
        role="doctor",
        hashed_password=get_password_hash("doctorpassword1"),
        hospital_id=1,  # Assigning hospital1
    )
    doctor2 = Doctor(
        name="Dr. Idris Omollo",
        email="idris@dawachat.ai",
        role="doctor",
        hashed_password=get_password_hash("doctorpassword2"),
        hospital_id=2,  # Assigning hospital2
    )
    doctor3 = Doctor(
        name="Dr. Enock Omwami",
        email="enock@dawachat.ai",
        role="doctor",
        hashed_password=get_password_hash("doctorpassword3"),
        hospital_id=1,  # Assigning hospital1
    )

    # Add to the session and commit
    db.add(super_admin)
    db.add_all([hospital1, hospital2, admin1, admin2, doctor1, doctor2, doctor3])
    db.commit()
    db.close()
    print("Database seeded with super_admin,hospitals, admins, and doctors.")

if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    Base.metadata.create_all(bind=engine)  # Recreate tables
    seed_database()
