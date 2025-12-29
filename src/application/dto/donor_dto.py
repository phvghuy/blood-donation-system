from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateDonorDTO:
    user_id: int
    full_name: str
    date_of_birth: str
    gender: str
    phone: str
    address: str
    blood_type_id: int

@dataclass
class UpdateDonorDTO:
    donor_id: int
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    blood_type_id: Optional[int] = None