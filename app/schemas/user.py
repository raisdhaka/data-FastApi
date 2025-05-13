from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    age: int
    phone: str
    email: Optional[str] = None
    residential_area: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # complaints: List["ComplaintResponse"] = []  # Forward reference

    class Config:
        orm_mode = True

# Resolve forward references after ComplaintResponse is defined
from app.schemas.complaint import ComplaintResponse  # Moved to bottom
UserResponse.update_forward_refs()