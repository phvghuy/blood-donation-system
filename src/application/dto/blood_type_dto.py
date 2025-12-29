from dataclasses import dataclass
from typing import Optional


@dataclass
class BloodTypeDTO:
    """Data Transfer Object for BloodType"""
    type_name: str
    id: Optional[int] = None


@dataclass
class BloodTypeCreateDTO:
    """DTO for creating a new blood type"""
    type_name: str


@dataclass
class BloodTypeResponseDTO:
    """DTO for blood type response"""
    id: int
    type_name: str

    @classmethod
    def from_entity(cls, blood_type):
        return cls(
            id=blood_type.id,
            type_name=blood_type.type_name
        )

