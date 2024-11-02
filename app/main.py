from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from .auth import authenticate_user, create_access_token
from .pdf_parser import parse_pdf
from .models import DosageDocument, Doctor
from .db import SessionLocal, engine

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
