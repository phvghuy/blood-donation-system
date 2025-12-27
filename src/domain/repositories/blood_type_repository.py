from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.blood_type import BloodType


class BloodTypeRepository(ABC):
    """Repository interface for BloodType entity"""

    @abstractmethod
    def create(self, blood_type: BloodType) -> BloodType:
        """Create a new blood type"""
        pass

    @abstractmethod
    def get_by_id(self, blood_type_id: int) -> Optional[BloodType]:
        """Get blood type by ID"""
        pass

    @abstractmethod
    def get_by_name(self, type_name: str) -> Optional[BloodType]:
        """Get blood type by name"""
        pass

    @abstractmethod
    def get_all(self) -> List[BloodType]:
        """Get all blood types"""
        pass

    @abstractmethod
    def update(self, blood_type: BloodType) -> BloodType:
        """Update blood type"""
        pass

    @abstractmethod
    def delete(self, blood_type_id: int) -> bool:
        """Delete blood type"""
        pass

    @abstractmethod
    def exists(self, type_name: str) -> bool:
        """Check if blood type exists"""
        pass

