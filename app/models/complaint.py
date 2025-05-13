from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,DateTime, Date, Time, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    complaint_name = Column(String(100), nullable=False)
    complaint_age = Column(Integer, nullable=False)
    area_of_complain = Column(String(100), nullable=False)
    type_of_incident = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    address = Column(Text, nullable=False)
    detail = Column(Text, nullable=False)
    criminal_name = Column(String(100), nullable=False)
    criminal_age = Column(Integer, nullable=False)
    criminal_gender = Column(String(50), nullable=False)
    relation = Column(String(100), nullable=False)
    is_physical_hit = Column(Boolean, nullable=False)
    physical_hit_detail = Column(Text)
    supporting_documents = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="complaints")