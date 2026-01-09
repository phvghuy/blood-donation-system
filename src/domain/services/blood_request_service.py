from typing import List
from src.domain.repositories.blood_request_repo import BloodRequestRepository
from src.domain.models.blood_request import BloodRequest


class BloodRequestService:
    def __init__(self, repo: BloodRequestRepository):
        self.repo = repo

    def create_request(self, user_id: int, blood_type_id: int, quantity: int) -> BloodRequest:
        if quantity <= 0:
            raise ValueError("Số lượng yêu cầu cần lớn hơn 0")

        return self.repo.create_request(user_id, blood_type_id, quantity)

    def get_hospital_history(self, user_id: int) -> List[BloodRequest]:
        return self.repo.get_requests_by_hospital_user(user_id)

    def get_pending_requests(self) -> List[BloodRequest]:
        return self.repo.get_pending_requests()

    def update_request_status(self, request_id: int, status: str) -> BloodRequest:
        if status not in ['approved', 'rejected']:
            raise ValueError("Trạng thái không hợp lệ (chỉ chấp nhận 'approved' hoặc 'rejected')")

        return self.repo.process_request(request_id, status)