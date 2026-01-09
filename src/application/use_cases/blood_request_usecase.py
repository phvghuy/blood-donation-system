from typing import List
from src.application.dto.request_dto import CreateRequestDTO, ProcessRequestDTO
from src.domain.services.blood_request_service import BloodRequestService
from src.domain.models.blood_request import BloodRequest

class BloodRequestUseCase:
    # Inject Service vào đây
    def __init__(self, service: BloodRequestService):
        self.service = service

    def send_request(self, dto: CreateRequestDTO) -> BloodRequest:
        return self.service.create_request(
            user_id=dto.user_id,
            blood_type_id=dto.blood_type_id,
            quantity=dto.quantity
        )

    def get_hospital_history(self, user_id: int) -> List[BloodRequest]:
        return self.service.get_hospital_history(user_id)

    def get_pending_requests(self) -> List[BloodRequest]:
        return self.service.get_pending_requests()

    def process_request(self, dto: ProcessRequestDTO) -> BloodRequest:
        return self.service.update_request_status(
            request_id=dto.request_id,
            status=dto.status
        )