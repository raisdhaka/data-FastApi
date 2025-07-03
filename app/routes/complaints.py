import re
import secrets
import string
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.complaint import ComplaintCreate, ComplaintResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.complaint_service import ComplaintService
from app.services.user_service import UserService
from app.database import get_db
from typing import List
from app import security


router = APIRouter(
    prefix="/complaints",
    tags=["complaints"]
)

def generate_username(name: str) -> str:
    """Generate username from name by replacing spaces with hyphens"""
    # Remove special characters and replace spaces with hyphens
    username = re.sub(r'[^a-zA-Z0-9 ]', '', name).strip()
    username = re.sub(r'\s+', '-', username).lower()
    
    # Ensure username is not empty
    if not username:
        username = "user" + ''.join(secrets.choice(string.digits) for _ in range(4))
    
    return username

def generate_password(email: str, phone: str) -> str:
    """Generate password using email if available, otherwise phone"""
    if email:
        return email  # In real app, you'd use a better method
    return phone  # Fallback to phone if no email

@router.post("/", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint_with_user(data: dict, db: Session = Depends(get_db)):
    # Generate username and password
    username = generate_username(data["name"])
    password = generate_password(data.get("email"), data["mobile"])
    
    # Extract user-related data
    user_data = {
        "name": data["name"],
        "age": data["age"],
        "email": data.get("email"),  # Email might be optional
        "phone": data["mobile"],
        "residential_area": data["residential_area"],
        "username": username,
        "password": password
    }
    
    # Check if email exists
    if user_data["email"] and UserService.get_user_by_email(db, user_data["email"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    if UserService.get_user_by_username(db, user_data["username"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create the user
    user = UserService.create_user(db=db, user=UserCreate(**user_data))
    
    # Extract complaint-related data
    complaint_data = {
        "complaint_name": data["complaint_name"],
        "complaint_age": data["complaint_age"],
        "area_of_complain": data["area_of_complain"],
        "type_of_incident": data["type_of_incident"],
        "date": data["date"],
        "time": data["time"],
        "address": data["area_of_complain"],
        "detail": data["detail"],
        "criminal_name": data["criminal_name"],
        "criminal_age": data["criminal_age"],
        "criminal_gender": data["criminal_gender"],
        "relation": data["relation"],
        "is_physical_hit": data["is_physical_hit"],
        "physical_hit_detail": data["physical_hit_detail"],
        "supporting_documents": data["supporting_documents"],
        "user_id": user.id  # Associate the complaint with the created user
    }
    
    # Create the complaint
    complaint = ComplaintService.create_complaint(db=db, complaint=ComplaintCreate(**complaint_data))
    
    # For security, remove password-related fields before returning
    user.hashed_password = None
    complaint.user = user
    
    return complaint

@router.get("/user/{user_id}", response_model=List[ComplaintResponse])
def get_complaints_by_user(user_id: int, db: Session = Depends(get_db)):
    complaints = ComplaintService.get_complaints_by_user(db=db, user_id=user_id)
    if not complaints:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No complaints found for this user"
        )
    return complaints

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    complaint = ComplaintService.get_complaint(db=db, complaint_id=complaint_id)
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    return complaint


@router.get("/", response_model=List[ComplaintResponse])
def get_all_complaints(db: Session = Depends(get_db)):
    complaints = ComplaintService.get_all_complaints(db=db)
    if not complaints:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No complaints found"
        )
    return complaints