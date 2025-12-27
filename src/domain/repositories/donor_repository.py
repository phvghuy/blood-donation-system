from abc import ABC, abstractmethod
from typing import Optional, List
from ..models.donor import Donor


class DonorRepository(ABC):
    """Repository interface for Donor entity"""

    @abstractmethod
    def create(self, donor: Donor) -> Donor:
        """Create a new donor"""
        pass

    @abstractmethod
    def get_by_id(self, donor_id: int) -> Optional[Donor]:
        """Get donor by ID"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Donor]:
        """Get donor by user ID"""
        pass

    @abstractmethod
    def get_by_phone(self, phone: str) -> Optional[Donor]:
        """Get donor by phone number"""
        pass

    @abstractmethod
    def get_all(self) -> List[Donor]:
        """Get all donors"""
        pass

    @abstractmethod
    def update(self, donor: Donor) -> Donor:
        """Update donor"""
        pass

    @abstractmethod
    def delete(self, donor_id: int) -> bool:
        """Delete donor"""
        pass

    @abstractmethod
    def exists_by_user_id(self, user_id: int) -> bool:
        """Check if donor exists by user ID"""
        pass

    @abstractmethod
    def exists_by_phone(self, phone: str) -> bool:
        """Check if donor exists by phone"""
        pass

    @abstractmethod
    def search_by_name(self, name: str) -> List[Donor]:
        """Search donors by name"""
        pass

    @abstractmethod
    def get_by_blood_type(self, blood_type_id: int) -> List[Donor]:
        """Get donors by blood type"""
        pass

