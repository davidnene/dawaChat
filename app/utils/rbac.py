from fastapi import HTTPException, status
from models import Doctor, Admin
from sqlalchemy.orm import Session

def verify_role(user, required_role: str):
    """
    Check if the current user has the required role.
    :param user: Current user object (Doctor or Admin)
    :param required_role: Role to check (e.g., "super_admin", "doctor")
    :return: Raises HTTPException if the role does not match.
    """
    if user.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required role: {required_role}",
        )

def is_super_admin(user):
    """
    Checks if the user is a super admin.
    :param user: Current user object (Doctor or Admin)
    :return: Raises HTTPException if the user is not a super admin.
    """
    verify_role(user, "super_admin")

def is_doctor(user):
    """
    Checks if the user is a doctor.
    :param user: Current user object (Doctor or Admin)
    :return: Raises HTTPException if the user is not a doctor.
    """
    verify_role(user, "doctor")

def can_create_doctor(current_user, db: Session):
    """
    Check if the current user can create a doctor account (i.e., is a super admin).
    :param current_user: The user requesting to create the doctor
    :param db: The database session
    :return: Raises HTTPException if the user cannot create a doctor.
    """
    is_super_admin(current_user)  # Check if the user is a super admin

def can_create_admin(current_user, db: Session):
    """
    Check if the current user can create a super admin account.
    :param current_user: The user requesting to create a super admin
    :param db: The database session
    :return: Raises HTTPException if the user cannot create a super admin.
    """
    is_super_admin(current_user)  # Ensure only super admin can create another super admin
