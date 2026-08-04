from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..logger import logger
from ..services import pets as pets_service

router = APIRouter(
    prefix="/api/v1/pets",
    tags=["Pets"]
)

# --- POST: Create Pet ---
@router.post("/", response_model=schemas.PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet(pet_data: schemas.PetCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new pet: {pet_data.name} (Type: {pet_data.type})")
    
    new_pet = pets_service.create_pet(db, pet_data)
    
    logger.debug(f"Successfully created pet (ID: {new_pet.id}).")
    return new_pet

# --- GET: All Pets ---
@router.get("/", response_model=List[schemas.PetResponse])
def get_all_pets(db: Session = Depends(get_db)):
    logger.info("Fetching all pets from the database.")
    
    pets = pets_service.get_all_pets(db)
    
    logger.debug(f"Retrieved {len(pets)} pets.")
    return pets

# --- GET: Pet by ID ---
@router.get("/{pet_id}", response_model=schemas.PetResponse)
def get_pet_by_id(pet_id: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching pet by ID: {pet_id}")
    
    pet = pets_service.get_pet_by_id(db, pet_id)
    
    if not pet:
        logger.warning(f"Pet lookup failed. ID {pet_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
        
    return pet

# --- DELETE: Delete Pet ---
@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(pet_id: str, db: Session = Depends(get_db)):
    logger.info(f"Attempting to delete pet ID: {pet_id}")
    
    success = pets_service.delete_pet(db, pet_id)
    
    if not success:
        logger.warning(f"Pet deletion failed. ID {pet_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
        
    logger.info(f"Successfully deleted pet ID: {pet_id}")
    return 