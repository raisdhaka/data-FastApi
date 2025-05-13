from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.complaint import ComplaintCreate, ComplaintResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.complaint_service import ComplaintService
from app.services.user_service import UserService
from app.database import get_db
from typing import List

router = APIRouter(
    prefix="/complaints",
    tags=["complaints"]
)

@router.post("/", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint_with_user(data: dict, db: Session = Depends(get_db)):
    # Extract user-related data
    user_data = {
        "name": data["name"],
        "age": data["age"],
        "email": data["email"],
        "phone": data["mobile"],
        "residential_area": data["residential_area"]
    }
    
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
    db.refresh(complaint)  # Only if needed
    complaint.user = None  # Break the cycle
    
    return complaint  # Return the complaint object instead of user.id

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