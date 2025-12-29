from src.application.dto.donation_event_dto import CreateDonationEventInputDTO
from src.domain.services.donation_event_service import DonationEventService

class CreateDonationEventUseCase:
    def __init__(self, service: DonationEventService):
        self.service = service

    def execute(self, input_dto: CreateDonationEventInputDTO):
        saved_event, saved_blood_unit = self.service.process_new_donation(
            donor_id=input_dto.donor_id,
            blood_type_id=input_dto.blood_type_id,
            donation_date=input_dto.donation_date,
            location=input_dto.location
        )

        return {
            "event_id": saved_event.id,
            "blood_unit_id": saved_blood_unit.id,
            "expiry_date": saved_blood_unit.expiry_date,
            "status": saved_blood_unit.status
        }