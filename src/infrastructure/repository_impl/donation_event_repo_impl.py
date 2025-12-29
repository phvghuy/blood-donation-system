from src.domain.models.donation_event import DonationEvent
from src.domain.repositories.donation_event_repo import DonationEventRepository
from src.infrastructure.orm.donation_event_model import DonationEventModel


class DonationEventRepositoryImpl(DonationEventRepository):
    def save(self, event: DonationEvent) -> DonationEvent:
        orm_model = DonationEventModel(
            donor_id=event.donor_id,
            blood_unit_id=event.blood_unit.id,
            location=event.location
        )

        orm_model.save()

        event.id = orm_model.id
        event.event_date = orm_model.event_date
        return event