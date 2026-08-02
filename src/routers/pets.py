from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Imported schemas alongside models
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(
    prefix="/api/v1/pets",
    tags=["Pets"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- POST: Add Pet ---
@router.post("/", response_model=schemas.PetResponse, status_code=status.HTTP_201_CREATED)
def add_pet(pet_data: schemas.PetCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == pet_data.user_guid).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    new_pet = models.Pet(type=pet_data.type, name=pet_data.name, user_guid=pet_data.user_guid)
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet

# --- GET: Get all pets ---
@router.get("/", response_model=List[schemas.PetResponse])
def get_all_pets(db: Session = Depends(get_db)):
    pets = db.query(models.Pet).all()
    return pets

# --- GET: Get pets by user id ---
@router.get("/get-pets-by-userid/{userId}", response_model=List[schemas.PetResponse])
def get_pets_by_userid(userId: str, db: Session = Depends(get_db)):
    pets = db.query(models.Pet).filter(models.Pet.user_guid == userId).all()
    return pets

# --- DELETE: Remove pet ---
@router.delete("/{pet_id}")
def remove_pet(pet_id: str, db: Session = Depends(get_db)):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
        
    db.delete(pet)
    db.commit()
    return {"message": f"Pet {pet_id} deleted successfully"}

# --- PUT: Update (Full) ---
@router.put("/{pet_id}", response_model=schemas.PetResponse)
def update_pet(pet_id: str, pet_data: schemas.PetCreate, db: Session = Depends(get_db)):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    
    user = db.query(models.User).filter(models.User.id == pet_data.user_guid).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="New assigned User not found")
        
    pet.type = pet_data.type
    pet.name = pet_data.name
    pet.user_guid = pet_data.user_guid
    
    db.commit()
    db.refresh(pet)
    return pet

# --- PATCH: Partial Update ---
@router.patch("/{pet_id}", response_model=schemas.PetResponse)
def patch_pet(pet_id: str, pet_data: schemas.PetPatch, db: Session = Depends(get_db)):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
        
    pet.name = pet_data.name
    db.commit()
    db.refresh(pet)
    return pet