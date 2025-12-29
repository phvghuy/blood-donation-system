from dataclasses import dataclass

@dataclass
class CreateRequestDTO:
    user_id: int
    blood_type_id: int
    quantity: int

@dataclass
class ProcessRequestDTO:
    request_id: int
    status: str