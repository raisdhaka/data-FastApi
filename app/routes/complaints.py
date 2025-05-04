from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.complaint import ComplaintCreate, ComplaintResponse
from app.services.complaint_service import ComplaintService
from app.database import get_db

router = APIRouter(
    prefix="/complaints",
    tags=["complaints"]
)

@router.post("/", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    return ComplaintService.create_complaint(db=db, complaint=complaint)

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