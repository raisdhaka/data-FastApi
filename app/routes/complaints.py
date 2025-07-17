import re
import secrets
import string
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.complaint import ComplaintCreate, ComplaintResponse
from app.schemas.user import UserCreate, UserResponse
from app.models.complaint import Complaint
from app.models.user import User
from app.services.complaint_service import ComplaintService
from app.services.user_service import UserService
from app.database import get_db
from typing import List
from app import security
from sqlalchemy import text
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from fastapi.security import OAuth2PasswordBearer
# from app.security import TokenData


router = APIRouter(
    prefix="/complaints",
    tags=["complaints"]
)

def generate_username(name: str, db: Session) -> str:
    """Generate unique username from name by replacing spaces with hyphens"""
    # Remove special characters and replace spaces with hyphens
    base_username = re.sub(r'[^a-zA-Z0-9 ]', '', name).strip()
    base_username = re.sub(r'\s+', '-', base_username).lower()
    
    # Ensure username is not empty
    if not base_username:
        base_username = "user"
    
    username = base_username
    counter = 1
    
    # Check if username exists and increment counter until we find a unique one
    while UserService.get_user_by_username(db, username):
        username = f"{base_username}-{counter}"
        counter += 1
    
    return username

def generate_password(email: str, phone: str) -> str:
    """Generate password using email if available, otherwise phone"""
    if email:
        return email  # In real app, you'd use a better method
    return phone  # Fallback to phone if no email

@router.post("/", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint_with_user(data: dict, db: Session = Depends(get_db)):
    # Generate username and password
    username = generate_username(data["name"], db)  # Pass db session here
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
    # if user_data["email"] and UserService.get_user_by_email(db, user_data["email"]):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email already registered"
    #     )
    
    # Check if username exists
    if UserService.get_user_by_username(db, user_data["username"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create the user
    user = UserService.create_user(db=db, user=UserCreate(**user_data))
    
    # Extract complaint-related data - ensure field names match ComplaintCreate schema
    complaint_data = {
        "complaint_name": data["complaint_name"],
        "complaint_age": data["complaint_age"],
        "area_of_complain": data["area_of_complain"],
        "type_of_incident": data["type_of_incident"],
        "date": data["date"],
        "time": data["time"],
        "address": data.get("address", ""),
        "detail": data["detail"],
        "criminal_name": data["criminal_name"],
        "criminal_age": data["criminal_age"],
        "criminal_gender": data["criminal_gender"],
        "relation": data["relation"],
        "is_physical_hit": data["is_physical_hit"],
        "physical_hit_detail": data.get("physical_hit_detail", ""),
        "supporting_documents": data.get("supporting_documents", ""),
        "user_id": user.id  # Make sure this matches the field name in ComplaintCreate
    }
    
    try:
        # Create the complaint
        complaint = ComplaintService.create_complaint(db=db, complaint=ComplaintCreate(**complaint_data))
        
        # Start email sending in background (non-blocking)
        
        try:
            sender_email = "support@aamarkatha.com"
            sender_password = "office@123"
            receiver_email = user_data["email"] if user_data.get("email") else "wfddhaka@gmail.com"
            
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Cc"] = "wfddhaka@gmail.com"  # Add CC properly
            message["Subject"] = "Your Complaint Has Been Registered"
            
            body = f"""
            Dear {user_data['name']},
            
            Your complaint has been successfully registered with the following details:
            
            Complaint ID: {complaint.id}
            Type of Incident: {complaint_data['type_of_incident']}
            Date: {complaint_data['date']}
            Time: {complaint_data['time']}
            Details: {complaint_data['detail']}

            For login, pls use the following credentials:
            Username: {user_data['username']}
            Password: {user_data['password']}

            Login UrL: https://aamarkatha.com/login
            
            We will review your complaint and get back to you soon.
            
            Thank you,
            Aamarkatha Team
            """
            
            message.attach(MIMEText(body, "plain"))
            
            # Use a thread to send email without blocking
            import threading
            def send_email_async():
                try:
                    with smtplib.SMTP_SSL("mail.privateemail.com", 465) as server:
                        server.login(sender_email, sender_password)
                        all_recipients = [receiver_email, "wfddhaka@gmail.com"]
                        server.sendmail(sender_email, all_recipients, message.as_string())
                except Exception as e:
                    print(f"Failed to send email: {str(e)}")
                    # Consider logging this properly
            
            # Start the email sending in background
            threading.Thread(target=send_email_async).start()
            
        except Exception as e:
            print(f"Email preparation failed: {str(e)}")

        # For security, remove password-related fields before returning
        user.hashed_password = None
        # complaint.user = user
        
        response_data = {
            "id": complaint.id,
            "complaint_name": complaint.complaint_name,
            "complaint_age": complaint.complaint_age,
            "area_of_complain": complaint.area_of_complain,
            "type_of_incident": complaint.type_of_incident,
            "date": complaint.date,
            "time": complaint.time,
            "address": complaint.address,
            "detail": complaint.detail,
            "criminal_name": complaint.criminal_name,
            "criminal_age": complaint.criminal_age,
            "criminal_gender": complaint.criminal_gender,
            "relation": complaint.relation,
            "is_physical_hit": complaint.is_physical_hit,
            "physical_hit_detail": complaint.physical_hit_detail,
            "supporting_documents": complaint.supporting_documents,
            "user_id": complaint.user_id,
            "created_at": complaint.created_at,
            "updated_at": complaint.updated_at,
            # Include minimal user info without complaints
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "age": user.age,
                "phone": user.phone,
                "residential_area": user.residential_area,
                "role": user.role
            }
        }

        return ComplaintResponse(**response_data)
        
    except Exception as e:
        # If complaint creation fails, rollback user creation
        db.delete(user)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create complaint: {str(e)}"
        )

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
    complaint = db.query(Complaint).options(joinedload(Complaint.user)).filter(Complaint.id == complaint_id).first()
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    return complaint

@router.get("/type_of_incident/statistics")
def get_complaints_count_by_type_of_incident(db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT type_of_incident, count(*) as count FROM complaints GROUP BY type_of_incident")
    )
    incidents = [{"type_of_incident": row[0], "count": row[1]} for row in result]
    
    if not incidents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No complaints found"
        )
    return incidents

@router.get("/", response_model=None)
def get_all_complaints(db: Session = Depends(get_db)):
    return db.query(Complaint).options(joinedload(Complaint.user)).all()
# def get_all_complaints(db: Session = Depends(get_db)):
#     complaints = ComplaintService.get_all_complaints(db=db)
#     if not complaints:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No complaints found"
#         )
#     return complaints


# Add this after the router initialization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/user-me/me", response_model=UserResponse)
def get_current_user_with_complaints(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    # Verify and decode the token
    token_data = security.verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get the user with complaints using joinedload
    user = db.query(User).options(joinedload(User.complaints)).filter(User.username == token_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create a minimal user response for the complaints
    user_minimal = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "age": user.age,
        "phone": user.phone,
        "residential_area": user.residential_area,
        "role": user.role
    }
    
    # Convert complaints to ComplaintResponse objects with user data
    complaint_responses = []
    for c in user.complaints:
        complaint_dict = {
            "id": c.id,
            "complaint_name": c.complaint_name,
            "complaint_age": c.complaint_age,
            "area_of_complain": c.area_of_complain,
            "type_of_incident": c.type_of_incident,
            "date": c.date,
            "time": c.time,
            "address": c.address,
            "detail": c.detail,
            "criminal_name": c.criminal_name,
            "criminal_age": c.criminal_age,
            "criminal_gender": c.criminal_gender,
            "relation": c.relation,
            "is_physical_hit": c.is_physical_hit,
            "physical_hit_detail": c.physical_hit_detail,
            "supporting_documents": c.supporting_documents,
            "user_id": c.user_id,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
            "user": user_minimal  # Include the user data
        }
        complaint_responses.append(ComplaintResponse(**complaint_dict))
    
    # Create the user response
    user_response = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        name=user.name,
        age=user.age,
        phone=user.phone,
        residential_area=user.residential_area,
        role=user.role,
        complaints=complaint_responses
    )
    
    return user_response