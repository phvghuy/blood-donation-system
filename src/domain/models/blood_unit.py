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
    donor_name: str = "Ẩn danh"

    def calculate_expiry_date(self):
        """
        Rule: Hạn dùng: 42 ngày kể từ ngày hiến
        """
        if self.donation_date:
            self.expiry_date = self.donation_date + timedelta(days=42)
        return self.expiry_date

    def mark_as_available(self):
        self.status = "available"

    # Kiểm tra tính hợp lệ khi đổi trạng thái
    def change_status(self, new_status: str):
        valid_statuses = ["available", "reserved", "used", "expired"]
        if new_status not in valid_statuses:
            raise ValueError(f"Trạng thái '{new_status}' không hợp lệ.")

        if self.status == "used" and new_status == "available":
            raise ValueError("Không thể tái sử dụng đơn vị máu đã dùng.")

        self.status = new_status