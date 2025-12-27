from typing import List, Optional
from datetime import date
from src.domain.models.donor import Donor
from src.domain.repositories.donor_repository import DonorRepository
from src.infrastructure.orm.donor_model import DonorModel


class DonorRepositoryImpl(DonorRepository):
    """Implementation of DonorRepository using Django ORM"""

    def create(self, donor: Donor) -> Donor:
        """Create a new donor"""
        donor_model = DonorModel.objects.create(
            user_id=donor.user_id,
            full_name=donor.full_name,
            date_of_birth=donor.date_of_birth,
            gender=donor.gender,
            phone=donor.phone,
            address=donor.address or "",
            blood_type_id=donor.blood_type_id
        )
        return self._to_entity(donor_model)

    def get_by_id(self, donor_id: int) -> Optional[Donor]:
        """Get donor by ID"""
        try:
            donor_model = DonorModel.objects.get(id=donor_id)
            return self._to_entity(donor_model)
        except DonorModel.DoesNotExist:
            return None

    def get_by_user_id(self, user_id: int) -> Optional[Donor]:
        """Get donor by user ID"""
        try:
            donor_model = DonorModel.objects.get(user_id=user_id)
            return self._to_entity(donor_model)
        except DonorModel.DoesNotExist:
            return None

    def get_by_phone(self, phone: str) -> Optional[Donor]:
        """Get donor by phone number"""
        try:
            donor_model = DonorModel.objects.get(phone=phone)
            return self._to_entity(donor_model)
        except DonorModel.DoesNotExist:
            return None

    def get_all(self) -> List[Donor]:
        """Get all donors"""
        donor_models = DonorModel.objects.all()
        return [self._to_entity(model) for model in donor_models]

    def update(self, donor: Donor) -> Donor:
        """Update donor"""
        donor_model = DonorModel.objects.get(id=donor.id)
        donor_model.full_name = donor.full_name
        donor_model.date_of_birth = donor.date_of_birth
        donor_model.gender = donor.gender
        donor_model.phone = donor.phone
        donor_model.address = donor.address or ""
        donor_model.blood_type_id = donor.blood_type_id
        donor_model.save()
        return self._to_entity(donor_model)

    def delete(self, donor_id: int) -> bool:
        """Delete donor"""
        try:
            donor_model = DonorModel.objects.get(id=donor_id)
            donor_model.delete()
            return True
        except DonorModel.DoesNotExist:
            return False

    def exists_by_user_id(self, user_id: int) -> bool:
        """Check if donor exists by user ID"""
        return DonorModel.objects.filter(user_id=user_id).exists()

    def exists_by_phone(self, phone: str) -> bool:
        """Check if donor exists by phone"""
        return DonorModel.objects.filter(phone=phone).exists()

    def search_by_name(self, name: str) -> List[Donor]:
        """Search donors by name"""
        donor_models = DonorModel.objects.filter(full_name__icontains=name)
        return [self._to_entity(model) for model in donor_models]

    def get_by_blood_type(self, blood_type_id: int) -> List[Donor]:
        """Get donors by blood type"""
        donor_models = DonorModel.objects.filter(blood_type_id=blood_type_id)
        return [self._to_entity(model) for model in donor_models]

    @staticmethod
    def _to_entity(model: DonorModel) -> Donor:
        """Convert ORM model to domain entity"""
        return Donor(
            id=model.id,
            user_id=model.user_id,
            full_name=model.full_name,
            date_of_birth=model.date_of_birth,
            gender=model.gender,
            phone=model.phone,
            address=model.address,
            blood_type_id=model.blood_type_id,
            created_at=model.created_at
        )

