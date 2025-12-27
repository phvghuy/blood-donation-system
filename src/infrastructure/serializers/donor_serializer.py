from rest_framework import serializers
from datetime import date


class DonorRegisterSerializer(serializers.Serializer):
    """Serializer for donor registration"""
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(max_length=100, required=True)
    gender = serializers.ChoiceField(
        choices=['male', 'female', 'other'],
        required=True
    )
    phone = serializers.CharField(max_length=20, required=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True)
    blood_type_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_username(self, value):
        """Validate username"""
        if len(value) < 3:
            raise serializers.ValidationError("Tên đăng nhập phải có ít nhất 3 ký tự")
        return value

    def validate_password(self, value):
        """Validate password strength"""
        if len(value) < 8:
            raise serializers.ValidationError("Mật khẩu phải có ít nhất 8 ký tự")
        return value

    def validate_full_name(self, value):
        """Validate full name"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Họ tên phải có ít nhất 2 ký tự")
        return value.strip()

    def validate_phone(self, value):
        """Validate phone number"""
        import re
        phone_pattern = r'^0\d{9,10}$'
        if not re.match(phone_pattern, value):
            raise serializers.ValidationError(
                "Số điện thoại không hợp lệ. Định dạng: 0XXXXXXXXX (10-11 số)"
            )
        return value

    def validate_date_of_birth(self, value):
        """Validate date of birth"""
        if value:
            today = date.today()
            age = today.year - value.year - (
                (today.month, today.day) < (value.month, value.day)
            )
            
            if age < 18:
                raise serializers.ValidationError("Người hiến máu phải từ 18 tuổi trở lên")
            
            if age > 65:
                raise serializers.ValidationError("Người hiến máu phải dưới 65 tuổi")
        
        return value


class DonorUpdateSerializer(serializers.Serializer):
    """Serializer for updating donor information"""
    full_name = serializers.CharField(max_length=100, required=False)
    gender = serializers.ChoiceField(
        choices=['male', 'female', 'other'],
        required=False
    )
    phone = serializers.CharField(max_length=20, required=False)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True)
    blood_type_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_full_name(self, value):
        """Validate full name"""
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError("Họ tên phải có ít nhất 2 ký tự")
        return value.strip() if value else value

    def validate_phone(self, value):
        """Validate phone number"""
        if value:
            import re
            phone_pattern = r'^0\d{9,10}$'
            if not re.match(phone_pattern, value):
                raise serializers.ValidationError(
                    "Số điện thoại không hợp lệ. Định dạng: 0XXXXXXXXX (10-11 số)"
                )
        return value

    def validate_date_of_birth(self, value):
        """Validate date of birth"""
        if value:
            today = date.today()
            age = today.year - value.year - (
                (today.month, today.day) < (value.month, value.day)
            )
            
            if age < 18:
                raise serializers.ValidationError("Người hiến máu phải từ 18 tuổi trở lên")
            
            if age > 65:
                raise serializers.ValidationError("Người hiến máu phải dưới 65 tuổi")
        
        return value


class DonorResponseSerializer(serializers.Serializer):
    """Serializer for donor response"""
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField()
    gender = serializers.CharField()
    phone = serializers.CharField()
    date_of_birth = serializers.DateField(allow_null=True)
    address = serializers.CharField(allow_null=True)
    blood_type_id = serializers.IntegerField(allow_null=True)
    blood_type_name = serializers.CharField(allow_null=True)
    age = serializers.IntegerField(allow_null=True)
    created_at = serializers.CharField(read_only=True)


class DonorLoginSerializer(serializers.Serializer):
    """Serializer for donor login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

