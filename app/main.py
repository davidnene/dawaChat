from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status, APIRouter
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from auth import authenticate_user, create_access_token, get_current_user
from schemas import LoginRequest
from db import SessionLocal
from routes import super_admin, admin, doctor, rag
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from utils.ML.process_doctor_stress_log import process_doctor_stress_log
import os
from utils.asdict import asdict


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = SessionLocal()
    yield  # The application runs while this is active
    app.state.db.close()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Initialize router 
app.include_router(super_admin.router)
app.include_router(admin.router)
app.include_router(doctor.router)
app.include_router(rag.router)

load_dotenv()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# OAuth2 password bearer setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Login Route for Authentication
@app.post("/api/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(login_request.email, login_request.password, db)
    if user.role == "doctor":
        process_doctor_stress_log(user.id, user.name, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(data={"sub": user.email, "role": user.role, "hospital": asdict(user.hospital), "name": user.name})
    return {"access_token": token, "token_type": "bearer"}

# Example of a route that requires super_admin role
@app.post("/api/super-admin-action")
def super_admin_action(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db, role="super_admin")
    
    return {"message": f"Super admin action performed by {current_user.email}"}

@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the DawaChat API"}