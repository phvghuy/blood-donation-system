from typing import List, Optional
from src.domain.models.donor import Donor
from src.domain.repositories.donor_repo import DonorRepository
from src.infrastructure.orm.donor_model import DonorModel
from src.infrastructure.orm.blood_unit_model import BloodUnitModel


class DonorRepositoryImpl(DonorRepository):

    def _to_entity(self, model: DonorModel) -> Donor:
        if not model:
            return None
        return Donor(
            id=model.id,
            user_id=model.user_id,
            full_name=model.full_name,
            date_of_birth=model.date_of_birth,
            gender=model.gender,
            phone=model.phone,
            address=model.address,
            blood_type_id=model.blood_type_id
        )

    def save(self, donor: Donor) -> Donor:
        # Tạo mới
        donor_model = DonorModel.objects.create(
            user_id=donor.user_id,
            full_name=donor.full_name,
            date_of_birth=donor.date_of_birth,
            gender=donor.gender,
            phone=donor.phone,
            address=donor.address,
            blood_type_id=donor.blood_type_id
        )
        return self._to_entity(donor_model)

    def get_by_id(self, donor_id: int) -> Optional[Donor]:
        try:
            model = DonorModel.objects.get(id=donor_id)
            return self._to_entity(model)
        except DonorModel.DoesNotExist:
            return None

    def update(self, donor: Donor) -> Donor:
        try:
            model = DonorModel.objects.get(id=donor.id)
            model.full_name = donor.full_name
            model.date_of_birth = donor.date_of_birth
            model.gender = donor.gender
            model.phone = donor.phone
            model.address = donor.address
            model.blood_type_id = donor.blood_type_id
            model.save()
            return self._to_entity(model)
        except DonorModel.DoesNotExist:
            raise Exception("Donor not found")

    def list_by_blood_type(self, blood_type_id: int) -> List[Donor]:
        models = DonorModel.objects.filter(blood_type_id=blood_type_id)
        return [self._to_entity(m) for m in models]

    def get_donation_history_ids(self, donor_id: int) -> List[int]:
        try:
            return list(BloodUnitModel.objects.filter(donor_id=donor_id).values_list('id', flat=True))
        except:
            return []