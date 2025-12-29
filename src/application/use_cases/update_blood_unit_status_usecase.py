from src.domain.services.blood_unit_service import BloodUnitService

class UpdateBloodUnitStatusUseCase:
    def __init__(self, service: BloodUnitService):
        self.service = service

    def execute(self, unit_id: int, new_status: str):
        return self.service.update_status(unit_id, new_status)