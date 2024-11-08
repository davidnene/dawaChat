from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime
from dotenv import load_dotenv
from auth import authenticate_user, create_access_token, get_password_hash, get_current_user
from pdf_parser import process_and_store_pdf_content
from models import DosageDocument, Doctor, Prescription
from db import SessionLocal
from query_handler import get_dosage_info
from schemas import DoctorCreate, LoginRequest, QueryDosageRequest
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import os


router = APIRouter()

app = FastAPI()

# Define origins that are allowed to make requests
origins = [
    "http://localhost:3000"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


load_dotenv()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Store the session in the app state
@app.on_event("startup")
async def startup_event():
    app.state.db = SessionLocal()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/api/create-doctor/", status_code=status.HTTP_201_CREATED)
async def create_doctor(
    doctor: DoctorCreate,
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    # Verify the token and get the current user
    current_user = get_current_user(token, db)  
    
    # Check if the current user is a super admin
    if current_user.role != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create doctor accounts")

    # Check if the email is already taken
    if db.query(Doctor).filter(Doctor.email == doctor.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use")

    # Create a new doctor account
    hashed_password = get_password_hash(doctor.password)
    new_doctor = Doctor(
        name=doctor.name,
        email=doctor.email,
        hashed_password=hashed_password,
        role="doctor"
    )

    # Add the new doctor to the database
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return {"message": f"Doctor {new_doctor.name} created successfully.", "doctor_id": new_doctor.id}
app.include_router(router)

@app.post("/api/upload-dosage-pdf/")
def upload_dosage_pdf(file: UploadFile = File(...), 
                      db: Session = Depends(get_db), 
                      token: str = Depends(oauth2_scheme)):
    
    # Verify the token and get the current user
    current_user = get_current_user(token, db)
    
    # Check if the current user is a super admin
    if current_user.role != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to upload documents")

     # Ensure /tmp directory exists
    tmp_dir = "/app/tmp"
    os.makedirs(tmp_dir, exist_ok=True)

    # Save file temporarily
    file_path = os.path.join(tmp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    # Parse and save to database
    process_and_store_pdf_content(file_path)
    dosage_document = DosageDocument(title=file.filename, content=file_path, uploaded_by=current_user.id)
    db.add(dosage_document)
    db.commit()
    return {"message": "Dosage PDF uploaded successfully"}

@app.post("/api/query-dosage/")
def query_dosage(
    request: QueryDosageRequest,  
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # Verify the token and get the current user
    current_user = get_current_user(token, db)
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    # Check if there is any existing dosage document in the system
    dosage_document = db.query(DosageDocument).order_by(DosageDocument.id.desc()).first()
    if not dosage_document:
        raise HTTPException(status_code=404, detail="No dosage document found")

    # Perform the query using the FAISS index loaded in get_dosage_info
    response = get_dosage_info(request.query)  
    return {"response": response}

@app.post("/api/prescribe/")
def create_prescription(patient_id: int, medication: str, dosage: str, frequency: str, notes: str, db: Session = Depends(get_db), current_user: Doctor = Depends(authenticate_user)):
    prescription = Prescription(
        patient_id=patient_id,
        doctor_id=current_user.id,
        medication=medication,
        dosage=dosage,
        frequency=frequency,
        notes=notes,
        timestamp=datetime.now()
    )
    db.add(prescription)
    db.commit()
    return {"message": "Prescription created successfully"}


@app.post("/api/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(login_request.email, login_request.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

