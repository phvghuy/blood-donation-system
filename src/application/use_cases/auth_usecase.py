from application.dto.auth_dto import RegisterDTO, LoginDTO
from domain.services.auth_service import AuthService

class AuthUseCase:
    def __init__(self):
        self.auth_service = AuthService()

    def register(self, dto: RegisterDTO):
        return self.auth_service.register_user(
            username=dto.username,
            password=dto.password,
            email=dto.email,
            role=dto.role
        )

    def login(self, dto: LoginDTO):
        return self.auth_service.authenticate_user(
            username=dto.username,
            password=dto.password
        )