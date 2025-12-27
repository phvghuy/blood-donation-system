from rest_framework import serializers


class BloodTypeSerializer(serializers.Serializer):
    """Serializer for BloodType"""
    id = serializers.IntegerField(read_only=True)
    type_name = serializers.CharField(max_length=10)

    def validate_type_name(self, value):
        """Validate blood type name"""
        valid_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Nhóm máu không hợp lệ. Phải là một trong: {', '.join(valid_types)}"
            )
        return value


class BloodTypeCreateSerializer(serializers.Serializer):
    """Serializer for creating blood type"""
    type_name = serializers.CharField(max_length=10)

    def validate_type_name(self, value):
        """Validate blood type name"""
        valid_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Nhóm máu không hợp lệ. Phải là một trong: {', '.join(valid_types)}"
            )
        return value

