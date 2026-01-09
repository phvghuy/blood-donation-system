from typing import List
from src.application.dto.blood_unit_dto import BloodUnitDTO
from src.domain.services.blood_unit_service import BloodUnitService


class GetBloodUnitsUseCase:
    def __init__(self, service: BloodUnitService):
        self.service = service

    def execute(self) -> List[BloodUnitDTO]:
        units = self.service.get_all_blood_units()

        return [
            BloodUnitDTO(
                id=u.id,
                blood_type=str(u.blood_type_id),
                status=u.status,
                expiry_date=u.expiry_date,
                donation_date=u.donation_date,
                status_display=u.status,
                donor_name=getattr(u, 'donor_name', "Ẩn danh")
            ) for u in units
        ]