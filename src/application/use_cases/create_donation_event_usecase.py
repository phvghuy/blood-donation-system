from src.domain.models.blood_unit import BloodUnit
from src.domain.models.donation_event import DonationEvent
from src.domain.repositories.blood_unit_repo import BloodUnitRepository
from src.domain.repositories.donation_event_repo import DonationEventRepository
from src.application.dto.donation_event_dto import CreateDonationEventInputDTO

class CreateDonationEventUseCase:
    def __init__(
        self,
        blood_unit_repo: BloodUnitRepository,
        donation_event_repo: DonationEventRepository
    ):
        self.blood_unit_repo = blood_unit_repo
        self.donation_event_repo = donation_event_repo

    def execute(self, input_dto: CreateDonationEventInputDTO):
        # Use Case 3: Xử lý Business Logic cho Blood Unit

        # Tạo Entity BloodUnit
        new_blood_unit = BloodUnit(
            donor_id=input_dto.donor_id,
            blood_type_id=input_dto.blood_type_id,
            donation_date=input_dto.donation_date
        )

        # Tính ngày hết hạn (42 ngày)
        new_blood_unit.calculate_expiry_date()

        new_blood_unit.mark_as_available()

        # Lưu Blood Unit vào kho
        saved_blood_unit = self.blood_unit_repo.save(new_blood_unit)

        # Use Case 2: Tạo sự kiện hiến máu

        # Tạo Entity DonationEvent
        new_event = DonationEvent(
            donor_id=input_dto.donor_id,
            blood_unit=saved_blood_unit,
            location=input_dto.location
        )

        # Lưu Donation Event
        saved_event = self.donation_event_repo.save(new_event)

        return {
            "event_id": saved_event.id,
            "blood_unit_id": saved_blood_unit.id,
            "expiry_date": saved_blood_unit.expiry_date,
            "status": saved_blood_unit.status
        }