from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from datetime import datetime
from .auth import authenticate_user, create_access_token
from .pdf_parser import parse_pdf
from .models import DosageDocument, Doctor, Prescription
from .db import SessionLocal, engine
from .query_handler import get_dosage_info

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload-dosage-pdf/")
def upload_dosage_pdf(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: Doctor = Depends(authenticate_user)):
    
    # Check if the current user is a super admin
    if current_user.role != "super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to upload documents")

    # Save file temporarily and parse
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    # Parse and save to database
    content = parse_pdf(file_path)
    dosage_document = DosageDocument(title=file.filename, content=content, uploaded_by=current_user.id)
    db.add(dosage_document)
    db.commit()
    return {"message": "Dosage PDF uploaded successfully"}

@app.get("/query-dosage/")
def query_dosage(query: str, db: Session = Depends(get_db), current_user: Doctor = Depends(authenticate_user)):
    # Ensure the user is authenticated as a doctor
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    # Check if there is any existing dosage document in the system
    dosage_document = db.query(DosageDocument).order_by(DosageDocument.id.desc()).first()
    if not dosage_document:
        raise HTTPException(status_code=404, detail="No dosage document found")

    # Perform the query using the FAISS index loaded in get_dosage_info
    response = get_dosage_info(query)
    return {"response": response}

@app.post("/prescribe/")
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

@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
