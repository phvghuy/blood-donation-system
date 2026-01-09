from datetime import datetime
from src.application.dto.donor_dto import CreateDonorDTO, UpdateDonorDTO
from src.domain.services.donor_service import DonorService


class DonorUseCase:
    def __init__(self, service: DonorService):
        self.service = service

    def create_donor(self, dto: CreateDonorDTO):
        dob = None
        if dto.date_of_birth:
            if isinstance(dto.date_of_birth, str):
                dob = datetime.strptime(dto.date_of_birth, '%Y-%m-%d').date()
            else:
                dob = dto.date_of_birth

        return self.service.create_new_donor(
            user_id=dto.user_id,
            full_name=dto.full_name,
            date_of_birth=dob,
            gender=dto.gender,
            phone=dto.phone,
            address=dto.address,
            blood_type_id=dto.blood_type_id
        )

    def update_donor_info(self, dto: UpdateDonorDTO):
        return self.service.update_donor_details(
            donor_id=dto.donor_id,
            full_name=dto.full_name,
            phone=dto.phone,
            address=dto.address,
            blood_type_id=dto.blood_type_id
        )

    def search_donors_by_blood_type(self, blood_type_id: int):
        return self.service.search_by_blood_type(blood_type_id)

    def get_donor_history(self, donor_id: int):
        donor, history_ids = self.service.get_donor_with_history(donor_id)

        return {
            "donor": donor,
            "donation_count": len(history_ids),
            "donation_unit_ids": history_ids
        }