from src.domain.repositories.blood_unit_repo import BloodUnitRepository
from src.domain.repositories.donation_event_repo import DonationEventRepository
from src.domain.repositories.blood_type_repo import BloodTypeRepository  # Giả định bạn có interface này
from src.domain.models.blood_unit import BloodUnit
from src.domain.models.donation_event import DonationEvent


class DonationEventService:
    def __init__(
            self,
            event_repo: DonationEventRepository,
            unit_repo: BloodUnitRepository,
            blood_type_repo: BloodTypeRepository
    ):
        self.event_repo = event_repo
        self.unit_repo = unit_repo
        self.blood_type_repo = blood_type_repo

    def process_new_donation(self, donor_id: int, blood_type_name: str, donation_date, location: str):
        # 1. Tìm ID nhóm máu từ tên (Logic chuyển từ View xuống đây)
        blood_type_id = self.blood_type_repo.get_id_by_name(blood_type_name)
        if not blood_type_id:
            raise ValueError(f"Loại máu '{blood_type_name}' không hợp lệ hoặc chưa được định nghĩa.")

        # 2. Tạo và xử lý Blood Unit (Entity Logic)
        new_blood_unit = BloodUnit(
            donor_id=donor_id,
            blood_type_id=blood_type_id,
            donation_date=donation_date,
            status="available"  # Hoặc status mặc định
        )
        # Tự động tính ngày hết hạn
        new_blood_unit.calculate_expiry_date()

        # Lưu Blood Unit
        saved_blood_unit = self.unit_repo.save(new_blood_unit)

        # 3. Tạo Donation Event (Entity Logic)
        new_event = DonationEvent(
            donor_id=donor_id,
            blood_unit=saved_blood_unit,  # Link với object vừa lưu
            location=location
        )

        # Lưu Donation Event
        saved_event = self.event_repo.save(new_event)

        return saved_event, saved_blood_unit