from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Donor:
    id: Optional[int]
    user_id: int
    full_name: str
    date_of_birth: Optional[date]
    gender: str
    phone: str
    address: str
    blood_type_id: Optional[int]
