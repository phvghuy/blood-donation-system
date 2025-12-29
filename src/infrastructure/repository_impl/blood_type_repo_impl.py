from src.domain.repositories.blood_type_repo import BloodTypeRepository
from src.infrastructure.orm.blood_type_model import BloodTypeModel

class BloodTypeRepositoryImpl(BloodTypeRepository):
    def get_id_by_name(self, name: str) -> int:
        return (
            BloodTypeModel.objects
            .only("id")
            .get(type_name=name)
            .id
        )
