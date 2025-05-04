from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time, Text, primary_key, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.complaint import Complaint


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100))
    residential_area = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    complaints = relationship("Complaint", back_populates="user")
