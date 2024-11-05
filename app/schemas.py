from pydantic import BaseModel, EmailStr

class DoctorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class LoginRequest(BaseModel):
    email: str
    password: str
    
class QueryDosageRequest(BaseModel):
    query: str