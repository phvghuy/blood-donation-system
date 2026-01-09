from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from src.presentation.permissions import IsHospital, IsAdmin

# Import các lớp Impl và Service, UseCase
from src.infrastructure.repository_impl.blood_unit_repo_impl import BloodUnitRepositoryImpl
from src.domain.services.blood_unit_service import BloodUnitService
from src.application.use_cases.get_blood_units_usecase import GetBloodUnitsUseCase
from src.application.use_cases.update_blood_unit_status_usecase import UpdateBloodUnitStatusUseCase
from src.infrastructure.serializers.blood_unit_serializer import (
    BloodUnitResponseSerializer,
    BloodUnitUpdateSerializer
)


# 1. View Lấy danh sách
class BloodUnitListView(APIView):
    permission_classes = [IsAuthenticated, IsHospital | IsAdmin]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # --- WIRING ---
        self.repo = BloodUnitRepositoryImpl()
        self.service = BloodUnitService(self.repo)
        self.use_case = GetBloodUnitsUseCase(self.service)

    def get(self, request):
        # Use Case trả về List[BloodUnitDTO]
        dtos = self.use_case.execute()

        # Serialize list DTO ra JSON
        # Lưu ý: Nếu Serializer của bạn dùng ModelSerializer, có thể cần chỉnh lại source
        # Nhưng thường thì Serializer vẫn hoạt động tốt với DTO object nếu trùng tên field
        data = [BloodUnitResponseSerializer(dto).data for dto in dtos]

        return Response(data, status=status.HTTP_200_OK)


# 2. View Cập nhật trạng thái
class BloodUnitStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsHospital | IsAdmin]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # --- WIRING ---
        self.repo = BloodUnitRepositoryImpl()
        self.service = BloodUnitService(self.repo)
        self.use_case = UpdateBloodUnitStatusUseCase(self.service)

    def patch(self, request, pk):
        # Dùng Serializer để validate input (new_status có hợp lệ không?)
        serializer = BloodUnitUpdateSerializer(data=request.data)

        if serializer.is_valid():
            new_status = serializer.validated_data['status']
            try:
                # Gọi Use Case
                updated_unit = self.use_case.execute(unit_id=pk, new_status=new_status)

                # Trả về kết quả
                return Response(
                    {"id": updated_unit.id, "status": updated_unit.status, "msg": "Updated successfully"},
                    status=status.HTTP_200_OK
                )
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)