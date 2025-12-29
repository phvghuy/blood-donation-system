from rest_framework import serializers
from src.infrastructure.orm.blood_unit_model import BloodUnitModel


class BloodUnitResponseSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    donor_name = serializers.CharField(source='donor.full_name', default="Ẩn danh", read_only=True)
    blood_type_display = serializers.StringRelatedField(source='blood_type', read_only=True)

    class Meta:
        model = BloodUnitModel
        fields = [
            'id',
            'donor_name',
            'blood_type_display',
            'donation_date',
            'expiry_date',
            'status',
            'status_display',
            'created_at'
        ]


class BloodUnitUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BloodUnitModel
        fields = ['status']  # Chỉ expose trường status

    def validate_status(self, value):
        if value not in dict(BloodUnitModel.STATUS_CHOICES):
            raise serializers.ValidationError("Trạng thái không hợp lệ.")
        return value