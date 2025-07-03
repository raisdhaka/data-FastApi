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
    username: str
    password: str  # Plaintext password for registration

class LoginCredentials(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    username: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # complaints: List["ComplaintResponse"] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

# Resolve forward references after ComplaintResponse is defined
from app.schemas.complaint import ComplaintResponse  # Moved to bottom
UserResponse.update_forward_refs()