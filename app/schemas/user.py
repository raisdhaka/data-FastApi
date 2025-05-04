from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.complaint import ComplaintResponse

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
    complaints: List[ComplaintResponse] = []

    class Config:
        orm_mode = True