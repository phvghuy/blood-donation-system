from dataclasses import dataclass
from datetime import date

@dataclass
class CreateDonationEventInputDTO:
    donor_id: int
    blood_type_name: str
    donation_date: date
    location: str