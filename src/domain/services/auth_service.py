from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class AuthService:
    def register_user(self, username, password, email, role):
        if role not in ["admin", "donor", "hospital"]:
            raise ValueError("Role không hợp lệ")

        if User.objects.filter(username=username).exists():
            raise ValueError("Tên đăng nhập đã tồn tại")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        if role == "admin":
            user.is_staff = True
            user.save()

        return user

    def authenticate_user(self, username, password):
        user = authenticate(
            username=username,
            password=password
        )

        if not user:
            raise ValueError("Sai tên đăng nhập hoặc mật khẩu")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "roles": list(user.groups.values_list("name", flat=True))
        }