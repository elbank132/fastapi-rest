from sqlalchemy.orm import Session
from .. import models, schemas

def create_pet(db: Session, pet_data: schemas.PetCreate):
    new_pet = models.Pet(
        name=pet_data.name,
        type=pet_data.type,
        user_guid=pet_data.user_guid
    )
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet

def get_all_pets(db: Session):
    return db.query(models.Pet).all()

def get_pet_by_id(db: Session, pet_id: str):
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()

def delete_pet(db: Session, pet_id: str) -> bool:
    pet = get_pet_by_id(db, pet_id)
    if not pet:
        return False
    
    db.delete(pet)
    db.commit()
    return True