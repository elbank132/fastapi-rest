import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), nullable=False)

    # Relationship: A user can have multiple pets
    pets = relationship("Pet", back_populates="owner")

class Pet(Base):
    __tablename__ = "pets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    type = Column(Integer, nullable=False)
    name = Column(String(15))
    
    user_guid = Column(String(36), ForeignKey("users.id"), nullable=False)

    # Relationship: A pet belongs to one user
    owner = relationship("User", back_populates="pets")