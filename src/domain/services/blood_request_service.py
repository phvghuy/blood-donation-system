from src.domain.repositories.blood_request_repo import BloodRequestRepository

class BloodRequestService:
    def __init__(self, repo: BloodRequestRepository):
        self.repo = repo

    def create_blood_request(self, user_id, blood_type_id, quantity):
        if quantity <= 0:
            raise ValueError("Số lượng yêu cầu cần lớn hơn 0")
        return self.repo.create_request(user_id, blood_type_id, quantity)

    def get_hospital_history(self, user_id):
        return self.repo.get_requests_by_hospital_user(user_id)

    def get_pending_requests(self):
        return self.repo.get_pending_requests()

    def update_request_status(self, request_id, status):
        if status not in ['approved', 'rejected']:
            raise ValueError("Cập nhật trạng thái không hợp lệ")
        return self.repo.process_request(request_id, status)