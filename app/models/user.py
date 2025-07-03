from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.complaint import Complaint


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # Authentication fields
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)  # Make nullable
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    # Profile fields
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=False)
    residential_area = Column(String(100), nullable=False)
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # Relationships
    complaints = relationship("Complaint", back_populates="user")
