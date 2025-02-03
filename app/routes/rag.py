from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from utils.rbac import verify_role
from db import get_db
from auth import get_current_user
from fastapi.security import OAuth2PasswordBearer
from utils.RAG.pdf_parser import process_and_store_pdf_content
from utils.RAG.query_handler import get_dosage_info
from models import DosageDocument
from schemas import QueryDosageRequest

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/api/upload-knmf/")
def upload_dosage_pdf(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "super_admin")
    
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    # Parse and save to database
    process_and_store_pdf_content(file_path)
    dosage_document = DosageDocument(title=file.filename, content=file_path, uploaded_by=current_user.id)
    db.add(dosage_document)
    db.commit()
    return {"message": "KNMF uploaded successfully"}

@router.post("/api/query-dosage/")
def query_dosage(
    request: QueryDosageRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    verify_role(current_user, "doctor")
    
     # Check if there is any existing dosage document in the system
    # dosage_document = db.query(DosageDocument).order_by(DosageDocument.id.desc()).first()
    # if not dosage_document:
    #     raise HTTPException(status_code=404, detail="No dosage document found")

    # Perform the query using the FAISS index loaded in get_dosage_info
    response = get_dosage_info(request.query)
    return {"response": response}