# src/presentation/views/hospital_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from src.presentation.permissions import IsAdmin # Tận dụng permission cũ

from src.infrastructure.repository_impl.hospital_repo_impl import HospitalRepositoryImpl
from src.application.use_cases.hospital_usecase import HospitalUseCase
from src.application.dto.hospital_dto import CreateHospitalDTO
from src.infrastructure.serializers.hospital_serializer import (
    HospitalRegisterSerializer,
    HospitalResponseSerializer
)

class HospitalListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = HospitalRepositoryImpl()
        self.use_case = HospitalUseCase(self.repo)

    # Lấy danh sách bệnh viện
    def get(self, request):
        hospitals = self.use_case.get_list_hospitals()
        data = [HospitalResponseSerializer(h).data for h in hospitals]
        return Response(data, status=status.HTTP_200_OK)

    # Thêm mới bệnh viện
    def post(self, request):
        serializer = HospitalRegisterSerializer(data=request.data)
        if serializer.is_valid():
            dto = CreateHospitalDTO(**serializer.validated_data)
            try:
                new_hospital = self.use_case.create_hospital(dto)
                # Dùng Serializer Output để trả về format đẹp
                return Response(
                    HospitalResponseSerializer(new_hospital).data,
                    status=status.HTTP_201_CREATED
                )
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HospitalDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = HospitalRepositoryImpl()
        self.use_case = HospitalUseCase(self.repo)

    # Xóa bệnh viện
    def delete(self, request, pk):
        try:
            self.use_case.delete_hospital(pk)
            return Response({"message": "Hospital deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)