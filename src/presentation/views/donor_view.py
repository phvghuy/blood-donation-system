from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from src.presentation.permissions import IsAdmin

from src.infrastructure.repository_impl.donor_repo_impl import DonorRepositoryImpl
from src.domain.services.donor_service import DonorService
from src.application.use_cases.donor_usecase import DonorUseCase
from src.application.dto.donor_dto import CreateDonorDTO, UpdateDonorDTO
from src.infrastructure.serializers.donor_serializer import DonorResponseSerializer, CreateDonorRequestSerializer


class DonorView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DonorRepositoryImpl()
        self.service = DonorService(self.repo)
        self.use_case = DonorUseCase(self.service)

    # 1. Tra cứu danh sách theo nhóm máu
    def get(self, request):
        blood_type_id = request.query_params.get('blood_type_id')
        if blood_type_id:
            donors = self.use_case.search_donors_by_blood_type(int(blood_type_id))
            data = [DonorResponseSerializer(d).data for d in donors]
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message": "Please provide blood_type_id"}, status=status.HTTP_400_BAD_REQUEST)

    # 2. Tạo hồ sơ người hiến máu
    def post(self, request):
        serializer = CreateDonorRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                dto = CreateDonorDTO(**serializer.validated_data)

                if dto.date_of_birth:
                    dto.date_of_birth = str(dto.date_of_birth)

                new_donor = self.use_case.create_donor(dto)
                return Response({"id": new_donor.id, "msg": "Created"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonorDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DonorRepositoryImpl()
        self.service = DonorService(self.repo)
        self.use_case = DonorUseCase(self.service)

    # 3. Xem lịch sử hiến máu
    def get(self, request, pk):
        try:
            result = self.use_case.get_donor_history(pk)

            donor_data = result['donor']
            if hasattr(donor_data, 'full_name'):
                donor_data = DonorResponseSerializer(donor_data).data
            else:
                donor_data = donor_data.__dict__

            data = {
                "donor": donor_data,
                "history": result['donation_unit_ids']
            }
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # 4. Cập nhật thông tin
    def put(self, request, pk):
        dto = UpdateDonorDTO(donor_id=pk, **request.data)
        try:
            updated_donor = self.use_case.update_donor_info(dto)
            return Response({"msg": "Updated successfully", "donor_id": updated_donor.id})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)