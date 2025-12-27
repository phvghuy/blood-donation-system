from typing import List, Optional
from src.domain.models.blood_type import BloodType
from src.domain.repositories.blood_type_repository import BloodTypeRepository
from src.infrastructure.orm.blood_type_model import BloodTypeModel


class BloodTypeRepositoryImpl(BloodTypeRepository):
    """Implementation of BloodTypeRepository using Django ORM"""

    def create(self, blood_type: BloodType) -> BloodType:
        """Create a new blood type"""
        blood_type_model = BloodTypeModel.objects.create(
            type_name=blood_type.type_name
        )
        return self._to_entity(blood_type_model)

    def get_by_id(self, blood_type_id: int) -> Optional[BloodType]:
        """Get blood type by ID"""
        try:
            blood_type_model = BloodTypeModel.objects.get(id=blood_type_id)
            return self._to_entity(blood_type_model)
        except BloodTypeModel.DoesNotExist:
            return None

    def get_by_name(self, type_name: str) -> Optional[BloodType]:
        """Get blood type by name"""
        try:
            blood_type_model = BloodTypeModel.objects.get(type_name=type_name)
            return self._to_entity(blood_type_model)
        except BloodTypeModel.DoesNotExist:
            return None

    def get_all(self) -> List[BloodType]:
        """Get all blood types"""
        blood_type_models = BloodTypeModel.objects.all()
        return [self._to_entity(model) for model in blood_type_models]

    def update(self, blood_type: BloodType) -> BloodType:
        """Update blood type"""
        blood_type_model = BloodTypeModel.objects.get(id=blood_type.id)
        blood_type_model.type_name = blood_type.type_name
        blood_type_model.save()
        return self._to_entity(blood_type_model)

    def delete(self, blood_type_id: int) -> bool:
        """Delete blood type"""
        try:
            blood_type_model = BloodTypeModel.objects.get(id=blood_type_id)
            blood_type_model.delete()
            return True
        except BloodTypeModel.DoesNotExist:
            return False

    def exists(self, type_name: str) -> bool:
        """Check if blood type exists"""
        return BloodTypeModel.objects.filter(type_name=type_name).exists()

    @staticmethod
    def _to_entity(model: BloodTypeModel) -> BloodType:
        """Convert ORM model to domain entity"""
        return BloodType(
            id=model.id,
            type_name=model.type_name
        )

