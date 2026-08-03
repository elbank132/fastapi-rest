from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..logger import logger

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

# --- POST: Create User ---
@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new user with name: {user_data.name}")
    
    new_user = models.User(name=user_data.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.debug(f"Successfully created user (ID: {new_user.id}).")
    return new_user

# --- GET: All Users ---
@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    logger.info("Fetching all users from the database.")
    users = db.query(models.User).all()
    logger.debug(f"Retrieved {len(users)} users.")
    return users

# --- GET: Users by Name ---
@router.get("/search/", response_model=List[schemas.UserResponse])
def get_users_by_name(name: str, db: Session = Depends(get_db)):
    logger.info(f"Searching for users matching name: '{name}'")
    users = db.query(models.User).filter(models.User.name.ilike(f"%{name}%")).all()
    logger.debug(f"Found {len(users)} users matching '{name}'.")
    return users

# --- DELETE: Users with no pets ---
@router.delete("/no-pets", status_code=status.HTTP_200_OK)
def remove_users_without_pets(db: Session = Depends(get_db)):
    logger.info("Attempting to delete all users with no assigned pets.")
    
    deleted_count = db.query(models.User).filter(~models.User.pets.any()).delete(synchronize_session=False)
    db.commit()
    
    logger.info(f"Successfully deleted {deleted_count} users without pets.")
    return {"message": f"Successfully deleted {deleted_count} users with no pets."}

# --- GET: User by ID ---
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching user by ID: {user_id}")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        logger.warning(f"User lookup failed. ID {user_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return user

# --- GET: User's Pets ---
@router.get("/{user_id}/pets", response_model=schemas.UserPetsDTO)
def get_user_pets(user_id: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching pets for user ID: {user_id}")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        logger.warning(f"Pet lookup failed. User ID {user_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    logger.debug(f"Successfully retrieved pets for user ID: {user_id}")
    return user