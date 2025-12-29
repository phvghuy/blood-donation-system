from src.domain.repositories.donor_repo import DonorRepository
from src.domain.models.donor import Donor


class DonorService:
    def __init__(self, donor_repo: DonorRepository):
        self.donor_repo = donor_repo

    def create_new_donor(self, user_id, full_name, date_of_birth, gender, phone, address, blood_type_id):
        new_donor = Donor(
            id=None,
            user_id=user_id,
            full_name=full_name,
            date_of_birth=date_of_birth,
            gender=gender,
            phone=phone,
            address=address,
            blood_type_id=blood_type_id
        )
        return self.donor_repo.save(new_donor)

    def update_donor_details(self, donor_id, full_name=None, phone=None, address=None, blood_type_id=None):
        current_donor = self.donor_repo.get_by_id(donor_id)
        if not current_donor:
            raise ValueError("Donor does not exist")

        if full_name:
            current_donor.full_name = full_name
        if phone:
            current_donor.phone = phone
        if address:
            current_donor.address = address
        if blood_type_id:
            current_donor.blood_type_id = blood_type_id

        return self.donor_repo.update(current_donor)

    def search_by_blood_type(self, blood_type_id: int):
        return self.donor_repo.list_by_blood_type(blood_type_id)

    def get_donor_with_history(self, donor_id: int):
        donor = self.donor_repo.get_by_id(donor_id)
        if not donor:
            raise ValueError("Donor not found")

        history_ids = self.donor_repo.get_donation_history_ids(donor_id)
        return donor, history_ids