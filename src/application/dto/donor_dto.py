from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class DonorCreateDTO:
    """DTO for creating a new donor"""
    username: str
    password: str
    email: str
    full_name: str
    gender: str
    phone: str
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    blood_type_id: Optional[int] = None


@dataclass
class DonorUpdateDTO:
    """DTO for updating donor information"""
    full_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    blood_type_id: Optional[int] = None


@dataclass
class DonorResponseDTO:
    """DTO for donor response"""
    id: int
    user_id: int
    username: str
    email: str
    full_name: str
    gender: str
    phone: str
    date_of_birth: Optional[date]
    address: Optional[str]
    blood_type_id: Optional[int]
    blood_type_name: Optional[str]
    age: Optional[int]
    created_at: str

    @classmethod
    def from_entity(cls, donor, user, blood_type_name=None):
        return cls(
            id=donor.id,
            user_id=donor.user_id,
            username=user.username,
            email=user.email,
            full_name=donor.full_name,
            gender=donor.gender,
            phone=donor.phone,
            date_of_birth=donor.date_of_birth,
            address=donor.address,
            blood_type_id=donor.blood_type_id,
            blood_type_name=blood_type_name,
            age=donor.get_age(),
            created_at=donor.created_at.isoformat() if donor.created_at else None
        )


@dataclass
class DonorLoginDTO:
    """DTO for donor login"""
    username: str
    password: str

