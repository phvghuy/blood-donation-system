from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.application.dto.donation_event_dto import CreateDonationEventInputDTO
from src.infrastructure.serializers.donation_event_serializer import CreateDonationEventSerializer
from src.presentation.permissions import IsAdmin

from src.infrastructure.repository_impl.blood_unit_repo_impl import BloodUnitRepositoryImpl
from src.infrastructure.repository_impl.donation_event_repo_impl import DonationEventRepositoryImpl
from src.infrastructure.repository_impl.blood_type_repo_impl import BloodTypeRepositoryImpl

from src.domain.services.donation_event_service import DonationEventService
from src.application.use_cases.create_donation_event_usecase import CreateDonationEventUseCase


class CreateDonationEventView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 1. Khởi tạo 3 Repositories cần thiết
        self.unit_repo = BloodUnitRepositoryImpl()
        self.event_repo = DonationEventRepositoryImpl()
        self.blood_type_repo = BloodTypeRepositoryImpl()

        # 2. Inject Repos vào Service
        self.service = DonationEventService(
            event_repo=self.event_repo,
            unit_repo=self.unit_repo,
            blood_type_repo=self.blood_type_repo
        )

        # 3. Inject Service vào UseCase
        self.use_case = CreateDonationEventUseCase(self.service)

    def post(self, request):
        serializer = CreateDonationEventSerializer(data=request.data)
        if serializer.is_valid():
            dto = CreateDonationEventInputDTO(
                donor_id=serializer.validated_data['donor_id'],
                blood_type_name=serializer.validated_data['blood_type'],
                donation_date=serializer.validated_data['donation_date'],
                location=serializer.validated_data.get('location', '')
            )

            try:
                result = self.use_case.execute(dto)
                return Response(result, status=status.HTTP_201_CREATED)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)