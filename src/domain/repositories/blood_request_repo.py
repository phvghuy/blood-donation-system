from abc import ABC, abstractmethod
from src.domain.models.blood_request import BloodRequest

class BloodRequestRepository(ABC):
    @abstractmethod
    def create_request(self, user_id, blood_type_id, quantity) -> BloodRequest:
        pass

    @abstractmethod
    def get_requests_by_hospital_user(self, user_id):
        pass

    @abstractmethod
    def get_pending_requests(self):
        pass

    @abstractmethod
    def process_request(self, request_id, new_status) -> BloodRequest:
        pass