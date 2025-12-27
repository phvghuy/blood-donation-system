from abc import ABC, abstractmethod
from src.domain.models.blood_unit import BloodUnit

class BloodUnitRepository(ABC):
    @abstractmethod
    def save(self, blood_unit: BloodUnit) -> BloodUnit:
        pass