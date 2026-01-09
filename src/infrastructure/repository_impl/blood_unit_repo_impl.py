from typing import List, Optional
from src.domain.models.blood_unit import BloodUnit
from src.domain.repositories.blood_unit_repo import BloodUnitRepository
from src.infrastructure.orm.blood_unit_model import BloodUnitModel


class BloodUnitRepositoryImpl(BloodUnitRepository):

    def _to_domain(self, orm_model: BloodUnitModel) -> BloodUnit:
        return BloodUnit(
            id=orm_model.id,
            blood_type_id=orm_model.blood_type_id,
            donor_id=orm_model.donor_id,
            donation_date=orm_model.donation_date,
            expiry_date=orm_model.expiry_date,
            status=orm_model.status,
            donor_name=orm_model.donor.full_name
        )

    def get_all(self) -> List[BloodUnit]:
        """Lấy danh sách tất cả túi máu"""
        qs = BloodUnitModel.objects.all()
        return [self._to_domain(item) for item in qs]

    def get_by_id(self, unit_id: int) -> Optional[BloodUnit]:
        """Lấy chi tiết một túi máu theo ID"""
        try:
            orm_model = BloodUnitModel.objects.get(id=unit_id)
            return self._to_domain(orm_model)
        except BloodUnitModel.DoesNotExist:
            return None

    def update(self, blood_unit: BloodUnit) -> None:
        """Cập nhật thông tin túi máu."""
        try:
            orm_model = BloodUnitModel.objects.get(id=blood_unit.id)

            orm_model.status = blood_unit.status
            orm_model.expiry_date = blood_unit.expiry_date

            orm_model.save()
        except BloodUnitModel.DoesNotExist:
            raise ValueError(f"BloodUnit với ID {blood_unit.id} không tồn tại để cập nhật.")

    def save(self, blood_unit: BloodUnit) -> BloodUnit:
        """Tạo mới túi máu"""
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