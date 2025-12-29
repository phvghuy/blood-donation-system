from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from src.infrastructure.repository_impl.blood_type_repository_impl import BloodTypeRepositoryImpl
from src.application.use_cases.manage_blood_type_usecase import ManageBloodTypeUseCase
from src.application.dto.blood_type_dto import BloodTypeCreateDTO
from src.infrastructure.serializers.blood_type_serializer import (
    BloodTypeSerializer,
    BloodTypeCreateSerializer
)


class BloodTypeListCreateView(APIView):
    """View for listing and creating blood types"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = BloodTypeRepositoryImpl()
        self.use_case = ManageBloodTypeUseCase(self.repository)

    def get(self, request):
        """Get all blood types"""
        try:
            blood_types = self.use_case.get_all_blood_types()
            serializer = BloodTypeSerializer(blood_types, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """Create a new blood type"""
        serializer = BloodTypeCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            dto = BloodTypeCreateDTO(**serializer.validated_data)
            blood_type = self.use_case.create_blood_type(dto)
            response_serializer = BloodTypeSerializer(blood_type)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BloodTypeDetailView(APIView):
    """View for retrieving, updating and deleting a blood type"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = BloodTypeRepositoryImpl()
        self.use_case = ManageBloodTypeUseCase(self.repository)

    def get(self, request, pk):
        """Get blood type by ID"""
        try:
            blood_type = self.use_case.get_blood_type_by_id(pk)
            if not blood_type:
                return Response(
                    {"error": "Không tìm thấy nhóm máu"},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = BloodTypeSerializer(blood_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        """Update blood type"""
        serializer = BloodTypeCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            dto = BloodTypeCreateDTO(**serializer.validated_data)
            blood_type = self.use_case.update_blood_type(pk, dto)
            response_serializer = BloodTypeSerializer(blood_type)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        """Delete blood type"""
        try:
            deleted = self.use_case.delete_blood_type(pk)
            if deleted:
                return Response(
                    {"message": "Xóa nhóm máu thành công"},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {"error": "Không tìm thấy nhóm máu"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BloodTypeInitializeView(APIView):
    """View for initializing standard blood types"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = BloodTypeRepositoryImpl()
        self.use_case = ManageBloodTypeUseCase(self.repository)

    def post(self, request):
        """Initialize all standard blood types"""
        try:
            blood_types = self.use_case.initialize_blood_types()
            serializer = BloodTypeSerializer(blood_types, many=True)
            return Response(
                {
                    "message": f"Đã khởi tạo {len(blood_types)} nhóm máu",
                    "blood_types": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

