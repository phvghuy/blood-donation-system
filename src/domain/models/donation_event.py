from dataclasses import dataclass
from datetime import datetime
from .blood_unit import BloodUnit

@dataclass
class DonationEvent:
    id: int = None
    donor_id: int = None
    blood_unit: BloodUnit = None
    event_date: datetime = None
    location: str = ""