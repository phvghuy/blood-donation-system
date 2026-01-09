from src.application.dto.donation_event_dto import CreateDonationEventInputDTO
from src.domain.services.donation_event_service import DonationEventService

class CreateDonationEventUseCase:
    def __init__(self, service: DonationEventService):
        self.service = service

    def execute(self, dto: CreateDonationEventInputDTO):
        event, unit = self.service.process_new_donation(
            donor_id=dto.donor_id,
            blood_type_name=dto.blood_type_name,
            donation_date=dto.donation_date,
            location=dto.location
        )

        return {
            "message": "Tạo sự kiện hiến máu thành công",
            "event_id": event.id,
            "blood_unit_id": unit.id,
            "expiry_date": unit.expiry_date,
            "status": unit.status
        }