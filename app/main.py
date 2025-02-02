from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status, APIRouter
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from auth import authenticate_user, create_access_token, get_current_user
from schemas import LoginRequest
from db import SessionLocal
from routes import super_admin  # Import the super_admin router
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

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


load_dotenv()

# Dependency to get the database session
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

# OAuth2 password bearer setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Login Route for Authentication
@app.post("/api/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(login_request.email, login_request.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

# Example of a route that requires super_admin role
@app.post("/api/super-admin-action")
def super_admin_action(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db, role="super_admin")
    
    return {"message": f"Super admin action performed by {current_user.email}"}
