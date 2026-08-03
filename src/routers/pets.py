from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Imported schemas alongside models
from .. import models, schemas
from ..database import get_db
from ..logger import logger

router = APIRouter(
    prefix="/api/v1/pets",
    tags=["Pets"]
)

# --- POST: Add Pet ---
@router.post("/", response_model=schemas.PetResponse, status_code=status.HTTP_201_CREATED)
def add_pet(pet_data: schemas.PetCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to create pet '{pet_data.name}' for user ID: {pet_data.user_guid}")
    
    user = db.query(models.User).filter(models.User.id == pet_data.user_guid).first()
    if not user:
        logger.warning(f"Pet creation failed. Assigned user ID {pet_data.user_guid} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    new_pet = models.Pet(type=pet_data.type, name=pet_data.name, user_guid=pet_data.user_guid)
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    
    logger.debug(f"Successfully created pet (ID: {new_pet.id}).")
    return new_pet

# --- GET: Get all pets ---
@router.get("/", response_model=List[schemas.PetResponse])
def get_all_pets(db: Session = Depends(get_db)):
    logger.info("Fetching all pets from the database.")
    pets = db.query(models.Pet).all()
    logger.debug(f"Retrieved {len(pets)} pets.")
    return pets

# --- GET: Get pets by user id ---
@router.get("/user/{user_id}", response_model=List[schemas.PetResponse])
def get_pets_by_userid(user_id: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching all pets belonging to user ID: {user_id}")
    pets = db.query(models.Pet).filter(models.Pet.user_guid == user_id).all()
    logger.debug(f"Found {len(pets)} pets for user ID: {user_id}.")
    return pets

# --- DELETE: Remove pet ---
@router.delete("/{pet_id}")
def remove_pet(pet_id: str, db: Session = Depends(get_db)):
    logger.info(f"Attempting to delete pet ID: {pet_id}")
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    
    if not pet:
        logger.warning(f"Delete failed. Pet ID {pet_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
        
    db.delete(pet)
    db.commit()
    
    logger.info(f"Successfully deleted pet ID: {pet_id}")
    return {"message": f"Pet {pet_id} deleted successfully"}

# --- PUT: Update (Full) ---
@router.put("/{pet_id}", response_model=schemas.PetResponse)
def update_pet(pet_id: str, pet_data: schemas.PetCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting full update (PUT) for pet ID: {pet_id}")
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    
    if not pet:
        logger.warning(f"Update failed. Pet ID {pet_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    
    user = db.query(models.User).filter(models.User.id == pet_data.user_guid).first()
    if not user:
        logger.warning(f"Update failed. New assigned User ID {pet_data.user_guid} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="New assigned User not found")
        
    pet.type = pet_data.type
    pet.name = pet_data.name
    pet.user_guid = pet_data.user_guid
    
    db.commit()
    db.refresh(pet)
    
    logger.debug(f"Successfully completed full update for pet ID: {pet_id}")
    return pet

# --- PATCH: Partial Update ---
@router.patch("/{pet_id}", response_model=schemas.PetResponse)
def patch_pet(pet_id: str, pet_data: schemas.PetPatch, db: Session = Depends(get_db)):
    logger.info(f"Attempting partial update (PATCH) for pet ID: {pet_id}")
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    
    if not pet:
        logger.warning(f"Patch failed. Pet ID {pet_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
        
    pet.name = pet_data.name
    db.commit()
    db.refresh(pet)
    
    logger.debug(f"Successfully completed partial update for pet ID: {pet_id}")
    return pet