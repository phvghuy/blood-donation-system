from dataclasses import dataclass
from datetime import date

@dataclass
class BloodUnitDTO:
    id: int
    blood_type: str
    status: str
    donation_date: date
    expiry_date: date
    status_display: str
    donor_name: str