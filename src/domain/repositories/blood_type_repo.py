from abc import ABC, abstractmethod

class BloodTypeRepository(ABC):
    @abstractmethod
    def get_id_by_name(self, name: str) -> int:
        pass
