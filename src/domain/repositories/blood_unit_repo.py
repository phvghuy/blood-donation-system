from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.blood_unit import BloodUnit

class BloodUnitRepository(ABC):
    @abstractmethod
    def save(self, blood_unit: BloodUnit) -> BloodUnit:
        pass

    @abstractmethod
    def get_all(self) -> List[BloodUnit]:
        pass

    @abstractmethod
    def get_by_id(self, unit_id: int) -> Optional[BloodUnit]:
        pass

    @abstractmethod
    def update(self, blood_unit: BloodUnit) -> None:
        pass