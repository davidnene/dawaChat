from models import Doctor, Admin
from db import SessionLocal, engine, Base
from auth import get_password_hash
from dotenv import load_dotenv

load_dotenv(override=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()

    # Check if the database is already seeded
    if db.query(Doctor).count() > 0 or db.query(Admin).count() > 0:
        print("Database already seeded")
        db.close()
        return

    # Create the super admin
    super_admin = Admin(
        name="Super Admin",
        email="superadmin@dawachat.ai",
        hashed_password=get_password_hash("SuperAdminPassword1"),
        role="super_admin"  # Ensure the `role` field exists in the `Admin` model
    )

    # Create an admin
    admin = Admin(
        name="Admin User",
        email="admin@dawachat.ai",
        hashed_password=get_password_hash("AdminPassword1"),
        role="admin"  # Ensure the `role` field exists in the `Admin` model
    )

    # Create doctors
    doctors = [
        Doctor(
            name="Dr. Rose Ochieng",
            email="rose@dawachat.ai",
            hashed_password=get_password_hash("DoctorPassword1"),
        ),
        Doctor(
            name="Dr. Idris Omollo",
            email="idris@dawachat.ai",
            hashed_password=get_password_hash("DoctorPassword1"),
        ),
        Doctor(
            name="Dr. Enock Omwami",
            email="enock@dawachat.ai",
            hashed_password=get_password_hash("DoctorPassword1"),
        ),
    ]

    # Add the records to the session
    db.add(super_admin)
    db.add(admin)
    db.add_all(doctors)

    # Commit the changes
    db.commit()
    db.close()

    print("Database seeded with super admin, admin, and doctors.")

if __name__ == "__main__":
    # Drop all tables and recreate them to start with a clean slate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_database()
