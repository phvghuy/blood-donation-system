from src.application.dto.hospital_dto import CreateHospitalDTO
from src.domain.services.hospital_service import HospitalService

class HospitalUseCase:
    def __init__(self, service: HospitalService):
        self.service = service

    def create_hospital(self, dto: CreateHospitalDTO):
        return self.service.create_new_hospital(
            username=dto.username,
            password=dto.password,
            email=dto.email,
            name=dto.name,
            phone=dto.phone,
            address=dto.address
        )

    def delete_hospital(self, hospital_id: int):
        return self.service.remove_hospital(hospital_id)

    def get_list_hospitals(self):
        return self.service.get_all_hospitals()