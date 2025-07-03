from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app import security
from typing import List


class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        # Hash password before storage
        hashed_password = security.get_password_hash(user.password)
        db_user = User(  # <-- Use User, not models.User
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            name=user.name,
            age=user.age,
            phone=user.phone,
            residential_area=user.residential_area
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_id(db, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_users(db: Session)-> List[User]:
        return db.query(User).all()
