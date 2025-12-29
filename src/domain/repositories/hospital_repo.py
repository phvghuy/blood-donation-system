from abc import ABC, abstractmethod
from typing import List
from src.domain.models.hospital import Hospital

class HospitalRepository(ABC):
    @abstractmethod
    def create_hospital(self, username, password, email, name, phone, address) -> Hospital:
        pass

    @abstractmethod
    def delete_hospital(self, hospital_id: int) -> bool:
        pass

    @abstractmethod
    def get_all_hospitals(self) -> List[Hospital]:
        pass

    @abstractmethod
    def get_hospital_by_id(self, hospital_id: int) -> Hospital:
        pass