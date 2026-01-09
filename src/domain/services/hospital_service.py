from typing import List
from src.domain.repositories.hospital_repo import HospitalRepository
from src.domain.models.hospital import Hospital


class HospitalService:
    def __init__(self, repo: HospitalRepository):
        self.repo = repo

    def create_new_hospital(self, username, password, email, name, phone, address) -> Hospital:
        return self.repo.create_hospital(
            username=username,
            password=password,
            email=email,
            name=name,
            phone=phone,
            address=address
        )

    def remove_hospital(self, hospital_id: int) -> bool:
        deleted = self.repo.delete_hospital(hospital_id)
        if not deleted:
            raise ValueError(f"Hospital with id {hospital_id} does not exist or could not be deleted")
        return True

    def get_all_hospitals(self) -> List[Hospital]:
        return self.repo.get_all_hospitals()

    def get_hospital_by_id(self, hospital_id: int) -> Hospital:
        hospital = self.repo.get_hospital_by_id(hospital_id)
        if not hospital:
            raise ValueError(f"Hospital with id {hospital_id} not found")
        return hospital