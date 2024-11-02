from pydantic import BaseModel, EmailStr

class DoctorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str