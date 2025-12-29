from typing import List
from src.domain.repositories.blood_unit_repo import BloodUnitRepository
from src.domain.models.blood_unit import BloodUnit

class BloodUnitService:
    def __init__(self, repo: BloodUnitRepository):
        self.repo = repo

    def get_all_blood_units(self) -> List[BloodUnit]:
        return self.repo.get_all()

    def update_status(self, unit_id: int, new_status: str):
        unit = self.repo.get_by_id(unit_id)
        if not unit:
            raise ValueError("Đơn vị máu không tồn tại")

        unit.change_status(new_status)

        return self.repo.update(unit)