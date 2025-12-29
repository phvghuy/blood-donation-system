from src.domain.models.blood_unit import BloodUnit
from src.domain.models.donation_event import DonationEvent
from src.domain.repositories.blood_unit_repo import BloodUnitRepository
from src.domain.repositories.donation_event_repo import DonationEventRepository

class DonationEventService:
    def __init__(
        self,
        blood_unit_repo: BloodUnitRepository,
        donation_event_repo: DonationEventRepository
    ):
        self.blood_unit_repo = blood_unit_repo
        self.donation_event_repo = donation_event_repo

    def process_new_donation(self, donor_id, blood_type_id, donation_date, location):
        new_blood_unit = BloodUnit(
            donor_id=donor_id,
            blood_type_id=blood_type_id,
            donation_date=donation_date
        )

        new_blood_unit.calculate_expiry_date()
        new_blood_unit.mark_as_available()

        saved_blood_unit = self.blood_unit_repo.save(new_blood_unit)

        new_event = DonationEvent(
            donor_id=donor_id,
            blood_unit=saved_blood_unit,
            location=location
        )

        saved_event = self.donation_event_repo.save(new_event)

        return saved_event, saved_blood_unit