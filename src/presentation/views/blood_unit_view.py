from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from src.presentation.permissions import IsHospital, IsAdmin

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
        dtos = self.use_case.execute()

        data = [BloodUnitResponseSerializer(dto).data for dto in dtos]

        return Response(data, status=status.HTTP_200_OK)


# 2. View Cập nhật trạng thái
class BloodUnitStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsHospital | IsAdmin]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = BloodUnitRepositoryImpl()
        self.service = BloodUnitService(self.repo)
        self.use_case = UpdateBloodUnitStatusUseCase(self.service)

    def patch(self, request, pk):
        serializer = BloodUnitUpdateSerializer(data=request.data)

        if serializer.is_valid():
            new_status = serializer.validated_data['status']
            try:
                updated_unit = self.use_case.execute(unit_id=pk, new_status=new_status)

                return Response(
                    {"id": updated_unit.id, "status": updated_unit.status, "msg": "Updated successfully"},
                    status=status.HTTP_200_OK
                )
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)