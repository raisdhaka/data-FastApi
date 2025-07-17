from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    age: int
    phone: str
    email: Optional[str] = None
    residential_area: Optional[str] = None
    role: Optional[str] = "user"

class UserCreate(UserBase):
    username: str
    password: str  # Plaintext password for registration


class LoginCredentials(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    residential_area: Optional[str] = None
    role: Optional[str] = "user"
    complaints: Optional[List["ComplaintResponse"]] = None
    
    class Config:
        from_attributes = True        


class Token(BaseModel):
    access_token: str
    token_type: str
    user_role: str
    user: str
    

# Resolve forward references after ComplaintResponse is defined
from app.schemas.complaint import ComplaintResponse  # Moved to bottom
UserResponse.update_forward_refs()