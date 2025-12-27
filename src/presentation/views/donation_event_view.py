from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Import DTO
from src.application.dto.donation_event_dto import CreateDonationEventInputDTO
# Import Use Case
from src.application.use_cases.create_donation_event_usecase import CreateDonationEventUseCase
# Import Serializer
from src.infrastructure.serializers.donation_event_serializer import CreateDonationEventSerializer
# Import Repos
from src.infrastructure.repository_impl.blood_unit_repo_impl import BloodUnitRepositoryImpl
from src.infrastructure.repository_impl.donation_event_repo_impl import DonationEventRepositoryImpl
from src.infrastructure.repository_impl.blood_type_repo_impl import BloodTypeRepositoryImpl

class CreateDonationEventView(APIView):
    def post(self, request):
        serializer = CreateDonationEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        blood_type_repo = BloodTypeRepositoryImpl()

        blood_type_id = blood_type_repo.get_id_by_name(
            serializer.validated_data["blood_type"]
        )

        input_dto = CreateDonationEventInputDTO(
            donor_id=serializer.validated_data['donor_id'],
            blood_type_id=blood_type_id,
            donation_date=serializer.validated_data['donation_date'],
            location=serializer.validated_data.get('location', '')
        )

        blood_unit_repo = BloodUnitRepositoryImpl()
        donation_event_repo = DonationEventRepositoryImpl()

        use_case = CreateDonationEventUseCase(
            blood_unit_repo=blood_unit_repo,
            donation_event_repo=donation_event_repo
        )

        try:
            result = use_case.execute(input_dto)
            return Response({
                "message": "Tạo sự kiện hiến máu thành công",
                "data": result
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)