from src.domain.models.blood_unit import BloodUnit
from src.domain.repositories.blood_unit_repo import BloodUnitRepository
from src.infrastructure.orm.blood_unit_model import BloodUnitModel

class BloodUnitRepositoryImpl(BloodUnitRepository):
    def save(self, blood_unit: BloodUnit) -> BloodUnit:
        orm_model = BloodUnitModel(
            donor_id=blood_unit.donor_id,
            blood_type_id=blood_unit.blood_type_id,
            donation_date=blood_unit.donation_date,
            expiry_date=blood_unit.expiry_date,
            status=blood_unit.status
        )

        orm_model.save()

        blood_unit.id = orm_model.id
        return blood_unit