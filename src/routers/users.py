from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Imported schemas alongside models
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- POST: Create User ---
@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(name=user_data.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- GET: All Users ---
@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# --- GET: Users by Name ---
@router.get("/search/", response_model=List[schemas.UserResponse])
def get_users_by_name(name: str, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.name.ilike(f"%{name}%")).all()
    return users

# --- GET: User by ID ---
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# --- GET: User's Pets ---
@router.get("/get-pets-by-id/{userId}", response_model=schemas.UserPetsDTO)
def get_user_pets(userId: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == userId).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

# --- DELETE: Users with no pets ---
@router.delete("/remove-no-pets")
def remove_users_without_pets(db: Session = Depends(get_db)):
    users_without_pets = db.query(models.User).filter(~models.User.pets.any()).all()
    
    deleted_count = len(users_without_pets)
    for user in users_without_pets:
        db.delete(user)
        
    db.commit()
    return {"message": f"Successfully deleted {deleted_count} users with no pets."}