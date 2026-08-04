from sqlalchemy.orm import Session
from .. import models, schemas

def create_user(db: Session, user_data: schemas.UserCreate):
    new_user = models.User(name=user_data.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_users_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name.ilike(f"%{name}%")).all()

def remove_users_without_pets(db: Session) -> int:
    deleted_count = db.query(models.User).filter(~models.User.pets.any()).delete(synchronize_session=False)
    db.commit()
    return deleted_count

def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()