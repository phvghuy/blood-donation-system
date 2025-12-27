from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from src.infrastructure.repository_impl.donor_repository_impl import DonorRepositoryImpl
from src.infrastructure.repository_impl.blood_type_repository_impl import BloodTypeRepositoryImpl
from src.application.use_cases.create_donor_usecase import CreateDonorUseCase
from src.application.dto.donor_dto import DonorCreateDTO, DonorUpdateDTO
from src.infrastructure.serializers.donor_serializer import (
    DonorRegisterSerializer,
    DonorUpdateSerializer,
    DonorResponseSerializer,
    DonorLoginSerializer
)


class DonorRegisterView(APIView):
    """View for donor registration"""
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.donor_repository = DonorRepositoryImpl()
        self.blood_type_repository = BloodTypeRepositoryImpl()
        self.use_case = CreateDonorUseCase(
            self.donor_repository,
            self.blood_type_repository
        )

    def post(self, request):
        """Register a new donor"""
        serializer = DonorRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            dto = DonorCreateDTO(**serializer.validated_data)
            donor = self.use_case.execute(dto)
            response_serializer = DonorResponseSerializer(donor)
            
            return Response(
                {
                    "message": "Đăng ký thành công",
                    "donor": response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Đã xảy ra lỗi: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DonorLoginView(APIView):
    """View for donor login"""
    permission_classes = [AllowAny]

    def post(self, request):
        """Login donor"""
        serializer = DonorLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response(
                {"error": "Tên đăng nhập hoặc mật khẩu không đúng"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Check if user has donor profile
        donor_repository = DonorRepositoryImpl()
        donor = donor_repository.get_by_user_id(user.id)
        
        if not donor:
            return Response(
                {"error": "Tài khoản không phải là người hiến máu"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Create or get token
        token, created = Token.objects.get_or_create(user=user)

        # Get blood type name
        blood_type_name = None
        if donor.blood_type_id:
            blood_type_repository = BloodTypeRepositoryImpl()
            blood_type = blood_type_repository.get_by_id(donor.blood_type_id)
            if blood_type:
                blood_type_name = blood_type.type_name

        from src.application.dto.donor_dto import DonorResponseDTO
        donor_data = DonorResponseDTO.from_entity(donor, user, blood_type_name)
        response_serializer = DonorResponseSerializer(donor_data)

        return Response(
            {
                "message": "Đăng nhập thành công",
                "token": token.key,
                "donor": response_serializer.data
            },
            status=status.HTTP_200_OK
        )


class DonorProfileView(APIView):
    """View for getting and updating donor profile"""
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.donor_repository = DonorRepositoryImpl()
        self.blood_type_repository = BloodTypeRepositoryImpl()
        self.use_case = CreateDonorUseCase(
            self.donor_repository,
            self.blood_type_repository
        )

    def get(self, request):
        """Get current donor profile"""
        try:
            donor_data = self.use_case.get_donor_by_user_id(request.user.id)
            response_serializer = DonorResponseSerializer(donor_data)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        """Update donor profile"""
        serializer = DonorUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get donor ID
            donor = self.donor_repository.get_by_user_id(request.user.id)
            if not donor:
                return Response(
                    {"error": "Không tìm thấy thông tin người hiến máu"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Update donor
            dto = DonorUpdateDTO(**serializer.validated_data)
            updated_donor = self.use_case.update_donor(donor.id, dto)
            response_serializer = DonorResponseSerializer(updated_donor)
            
            return Response(
                {
                    "message": "Cập nhật thông tin thành công",
                    "donor": response_serializer.data
                },
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


class DonorDetailView(APIView):
    """View for getting donor details by ID (admin)"""
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.donor_repository = DonorRepositoryImpl()
        self.blood_type_repository = BloodTypeRepositoryImpl()
        self.use_case = CreateDonorUseCase(
            self.donor_repository,
            self.blood_type_repository
        )

    def get(self, request, pk):
        """Get donor by ID"""
        try:
            donor_data = self.use_case.get_donor_by_id(pk)
            response_serializer = DonorResponseSerializer(donor_data)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

