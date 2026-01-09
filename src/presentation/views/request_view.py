from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from src.presentation.permissions import IsAdmin, IsHospital

from src.infrastructure.repository_impl.blood_request_repo_impl import BloodRequestRepositoryImpl
from src.domain.services.blood_request_service import BloodRequestService
from src.application.use_cases.blood_request_usecase import BloodRequestUseCase
from src.application.dto.request_dto import CreateRequestDTO, ProcessRequestDTO
from src.infrastructure.serializers.request_serializer import (
    CreateRequestSerializer,
    ProcessRequestSerializer,
    RequestResponseSerializer
)

# 1. API cho Bệnh viện (Hospital)
class HospitalRequestView(APIView):
    permission_classes = [IsAuthenticated, IsHospital]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = BloodRequestRepositoryImpl()
        self.service = BloodRequestService(self.repo) # Inject Repo vào Service
        self.use_case = BloodRequestUseCase(self.service) # Inject Service vào UseCase

    def get(self, request):
        requests = self.use_case.get_hospital_history(request.user.id)
        data = [RequestResponseSerializer(r).data for r in requests]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateRequestSerializer(data=request.data)
        if serializer.is_valid():
            dto = CreateRequestDTO(
                user_id=request.user.id,
                blood_type_id=serializer.validated_data['blood_type_id'],
                quantity=serializer.validated_data['quantity']
            )
            try:
                new_req = self.use_case.send_request(dto)
                return Response(RequestResponseSerializer(new_req).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. API cho Admin
class AdminRequestView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = BloodRequestRepositoryImpl()
        self.service = BloodRequestService(self.repo)
        self.use_case = BloodRequestUseCase(self.service)

    def get(self, request):
        requests = self.use_case.get_pending_requests()
        data = [RequestResponseSerializer(r).data for r in requests]
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        serializer = ProcessRequestSerializer(data=request.data)
        if serializer.is_valid():
            dto = ProcessRequestDTO(
                request_id=pk,
                status=serializer.validated_data['status']
            )
            try:
                result = self.use_case.process_request(dto)
                return Response({
                    "message": f"Request {result.status} successfully",
                    "data": RequestResponseSerializer(result).data
                }, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)