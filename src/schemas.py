from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List
from uuid import UUID

# ==========================================
# INPUT DTOs (For handling incoming requests)
# ==========================================

class UserCreate(BaseModel):
    name: str = Field(..., min_length=5, max_length=50)

class PetCreate(BaseModel):
    type: int
    name: str = Field(..., min_length=5, max_length=15)
    user_guid: UUID  

    @field_validator('type')
    @classmethod
    def type_must_not_be_zero(cls, v: int) -> int:
        if v == 0:
            raise ValueError('Pet type cannot be exactly 0')
        return v

class PetPatch(BaseModel):
    name: str = Field(..., min_length=5, max_length=15)

# ==========================================
# OUTPUT DTOs (For returning standard data)
# ==========================================

class UserResponse(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)

class PetResponse(BaseModel):
    id: UUID
    type: int
    name: str
    user_guid: UUID

    model_config = ConfigDict(from_attributes=True)

# ==========================================
# SPECIFIC DTOs (Pythonic Implementations)
# ==========================================

class PetDTO(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)

class UserPetsDTO(BaseModel):
    user_guid: UUID = Field(validation_alias='id')
    pets: List[PetDTO]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)