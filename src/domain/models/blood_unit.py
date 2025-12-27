from datetime import date, timedelta
from dataclasses import dataclass

@dataclass
class BloodUnit:
    id: int = None
    donor_id: int = None
    blood_type_id: int = None
    donation_date: date = None
    expiry_date: date = None
    status: str = "available"

    def calculate_expiry_date(self):
        """
        Rule: Hạn dùng: 42 ngày kể từ ngày hiến
        """
        if self.donation_date:
            self.expiry_date = self.donation_date + timedelta(days=42)
        return self.expiry_date

    def mark_as_available(self):
        self.status = "available"