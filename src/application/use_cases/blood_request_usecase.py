from src.application.dto.request_dto import CreateRequestDTO, ProcessRequestDTO
from src.domain.services.blood_request_service import BloodRequestService

class BloodRequestUseCase:
    def __init__(self, service: BloodRequestService):
        self.service = service

    def send_request(self, dto: CreateRequestDTO):
        return self.service.create_blood_request(
            user_id=dto.user_id,
            blood_type_id=dto.blood_type_id,
            quantity=dto.quantity
        )

    def get_hospital_history(self, user_id):
        return self.service.get_hospital_history(user_id)

    def get_pending_requests(self):
        return self.service.get_pending_requests()

    def process_request(self, dto: ProcessRequestDTO):
        return self.service.update_request_status(
            request_id=dto.request_id,
            status=dto.status
        )