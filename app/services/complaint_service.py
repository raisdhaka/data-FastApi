from sqlalchemy.orm import Session
from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintCreate

class ComplaintService:
    @staticmethod
    def create_complaint(db: Session, complaint: ComplaintCreate):
        db_complaint = Complaint(**complaint.dict())
        db.add(db_complaint)
        db.commit()
        db.refresh(db_complaint)
        return db_complaint

    @staticmethod
    def get_complaints_by_user(db: Session, user_id: int):
        return db.query(Complaint)\
                .filter(Complaint.user_id == user_id)\
                .all()

    @staticmethod
    def get_complaint(db: Session, complaint_id: int):
        return db.query(Complaint)\
                .filter(Complaint.id == complaint_id)\
                .first()