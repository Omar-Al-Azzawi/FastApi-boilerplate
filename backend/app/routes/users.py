from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserCreate, User as UserSchema
from app.models.users import User as UserModel
from app.core.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(UserModel).filter(
            (UserModel.username == user.username) | 
            (UserModel.email == user.email)
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already registered")
        
        new_user = UserModel(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return { "user": new_user, "message": "user created successfully"}
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user