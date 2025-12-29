from src.domain.repositories.hospital_repo import HospitalRepository

class HospitalService:
    def __init__(self, repo: HospitalRepository):
        self.repo = repo

    def register_hospital(self, username, password, email, name, phone, address):
        return self.repo.create_hospital(
            username=username,
            password=password,
            email=email,
            name=name,
            phone=phone,
            address=address
        )

    def remove_hospital(self, hospital_id: int):
        return self.repo.delete_hospital(hospital_id)

    def list_all_hospitals(self):
        return self.repo.get_all_hospitals()