from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.donor import Donor


class DonorRepository(ABC):

    @abstractmethod
    def save(self, donor: Donor) -> Donor:
        pass

    @abstractmethod
    def get_by_id(self, donor_id: int) -> Optional[Donor]:
        pass

    @abstractmethod
    def update(self, donor: Donor) -> Donor:
        pass

    @abstractmethod
    def list_by_blood_type(self, blood_type_id: int) -> List[Donor]:
        pass

    @abstractmethod
    def get_donation_history_ids(self, donor_id: int) -> List[int]:
        pass