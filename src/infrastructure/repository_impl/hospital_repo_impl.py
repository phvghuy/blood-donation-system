# src/infrastructure/repository_impl/hospital_repo_impl.py
from django.db import transaction
from django.contrib.auth.models import User, Group
from src.domain.repositories.hospital_repo import HospitalRepository
from src.domain.models.hospital import Hospital
from src.infrastructure.orm.hospital_model import HospitalModel # Import model bạn đã cung cấp


class HospitalRepositoryImpl(HospitalRepository):

    def _to_entity(self, model: HospitalModel):
        return Hospital(
            id=model.id,
            user_id=model.user.id,
            name=model.name,
            phone=model.phone,
            address=model.address,
            username=model.user.username
        )

    def create_hospital(self, username, password, email, name, phone, address) -> Hospital:
        try:
            with transaction.atomic():
                # 1. Tạo User login
                user = User.objects.create_user(username=username, email=email, password=password)

                group, _ = Group.objects.get_or_create(name='hospital')
                user.groups.add(group)

                # 2. Tạo Hospital Profile
                hospital_model = HospitalModel.objects.create(
                    user=user,
                    name=name,
                    phone=phone,
                    address=address
                )
                return self._to_entity(hospital_model)
        except Exception as e:
            raise ValueError(f"Error creating hospital: {str(e)}")

    def delete_hospital(self, hospital_id: int) -> bool:
        try:
            hospital = HospitalModel.objects.get(id=hospital_id)
            user = hospital.user
            # Xóa User
            user.delete()
            return True
        except HospitalModel.DoesNotExist:
            raise ValueError("Hospital not found")

    def get_all_hospitals(self):
        models = HospitalModel.objects.select_related('user').all().order_by('-created_at')
        return [self._to_entity(m) for m in models]

    def get_hospital_by_id(self, hospital_id: int) -> Hospital:
        try:
            model = HospitalModel.objects.select_related('user').get(id=hospital_id)
            return self._to_entity(model)
        except HospitalModel.DoesNotExist:
            raise ValueError("Hospital not found")