from abc import ABC, abstractmethod
from src.domain.models.donation_event import DonationEvent

class DonationEventRepository(ABC):
    @abstractmethod
    def save(self, event: DonationEvent) -> DonationEvent:
        pass