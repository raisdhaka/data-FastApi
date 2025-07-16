from datetime import date, time, datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.user import UserResponse 

class ComplaintBase(BaseModel):
    complaint_name: str
    complaint_age: int
    area_of_complain: str
    type_of_incident: str
    date: date
    time: time
    address: str
    detail: str
    criminal_name: str
    criminal_age: int
    criminal_gender: str
    relation: str
    is_physical_hit: bool
    physical_hit_detail: Optional[str] = None
    supporting_documents: Optional[str] = None
    user_id: int  # Keep only the ID reference
    


class ComplaintCreate(ComplaintBase):
    user_id: int

class ComplaintResponse(ComplaintBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    # user: "UserResponse"  # Forward reference
    user: Optional[UserResponse]

    class Config:
        orm_mode = True

# Resolve forward references after UserResponse is defined
from app.schemas.user import UserResponse  # Moved to bottom
ComplaintResponse.update_forward_refs()