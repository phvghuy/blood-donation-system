from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from infrastructure.serializers.auth_serializer import (
    RegisterSerializer, LoginSerializer
)
from application.use_cases.auth_usecase import AuthUseCase
from application.dto.auth_dto import RegisterDTO, LoginDTO


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = RegisterDTO(**serializer.validated_data)

        usecase = AuthUseCase()
        user = usecase.register(dto)

        role = user.groups.first().name if user.groups.exists() else None

        return Response({
            "message": "Đăng ký thành công",
            "user_id": user.id,
            "role": role
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = LoginDTO(**serializer.validated_data)

        usecase = AuthUseCase()
        token_data = usecase.login(dto)

        return Response(token_data, status=status.HTTP_200_OK)
