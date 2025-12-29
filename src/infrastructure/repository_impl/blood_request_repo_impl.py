from django.db import transaction
from src.domain.repositories.blood_request_repo import BloodRequestRepository
from src.domain.models.blood_request import BloodRequest

# Import Models
from src.infrastructure.orm.request_model import BloodRequestModel
from src.infrastructure.orm.blood_unit_model import BloodUnitModel
from src.infrastructure.orm.hospital_model import HospitalModel
from src.infrastructure.orm.blood_type_model import BloodTypeModel


class BloodRequestRepositoryImpl(BloodRequestRepository):

    def _to_entity(self, model: BloodRequestModel):
        return BloodRequest(
            id=model.id,
            hospital_name=model.hospital.name,
            blood_type_name=model.blood_type.type_name if model.blood_type else "Unknown",
            quantity=model.quantity,
            status=model.status,
            request_date=model.request_date
        )

    def create_request(self, user_id, blood_type_id, quantity):
        try:
            # 1. Tìm Hospital Profile từ User ID
            hospital = HospitalModel.objects.get(user_id=user_id)

            # 2. Tạo Request
            model = BloodRequestModel.objects.create(
                hospital=hospital,
                blood_type_id=blood_type_id,
                quantity=quantity,
                status='pending'
            )
            return self._to_entity(model)
        except Exception as e:
            raise ValueError(f"Error creating request: {str(e)}")

    def get_requests_by_hospital_user(self, user_id):
        # Filter qua bảng HospitalModel
        qs = BloodRequestModel.objects.filter(hospital__user_id=user_id).order_by('-request_date')
        return [self._to_entity(m) for m in qs]

    def get_pending_requests(self):
        qs = BloodRequestModel.objects.filter(status='pending').order_by('request_date')
        return [self._to_entity(m) for m in qs]

    def process_request(self, request_id, new_status):
        try:
            with transaction.atomic():
                req = BloodRequestModel.objects.select_for_update().get(id=request_id)

                if req.status != 'pending':
                    raise ValueError("Yêu cầu đã được xử lý")

                if new_status == 'approved':
                    # 1. Tìm các túi máu available cùng nhóm máu
                    # Sắp xếp theo expiry_date (Hết hạn trước xuất trước)
                    available_units = BloodUnitModel.objects.select_for_update().filter(
                        blood_type=req.blood_type,
                        status='available'
                    ).order_by('expiry_date')

                    # 2. Kiểm tra số lượng
                    count = available_units.count()
                    if count < req.quantity:
                        raise ValueError(f"Không đủ túi máu cho yêu cầu. Có sẵn: {count}, Yêu cầu: {req.quantity}")

                    # 3. Lấy đúng số lượng cần thiết
                    units_to_reserve = available_units.values_list('id', flat=True)[:req.quantity]

                    # 4. Update trạng thái các túi máu thành 'reserved'
                    BloodUnitModel.objects.filter(id__in=units_to_reserve).update(status='reserved')

                # Cập nhật trạng thái yêu cầu
                req.status = new_status
                req.save()

                return self._to_entity(req)

        except BloodRequestModel.DoesNotExist:
            raise ValueError("Không tìm thấy yêu cầu")