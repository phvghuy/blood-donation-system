# src/application/dto/hospital_dto.py
from dataclasses import dataclass

@dataclass
class CreateHospitalDTO:
    username: str
    password: str
    email: str
    name: str
    phone: str
    address: str