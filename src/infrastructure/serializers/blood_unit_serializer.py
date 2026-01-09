from rest_framework import serializers
from src.infrastructure.orm.blood_unit_model import BloodUnitModel


class BloodUnitResponseSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(read_only=True)
    blood_type = serializers.CharField(read_only=True)

    class Meta:
        model = BloodUnitModel
        fields = [
            'id',
            'donor_name',
            'blood_type',
            'donation_date',
            'expiry_date',
            'status',
        ]


class BloodUnitUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BloodUnitModel
        fields = ['status']  # Chỉ expose trường status

    def validate_status(self, value):
        if value not in dict(BloodUnitModel.STATUS_CHOICES):
            raise serializers.ValidationError("Trạng thái không hợp lệ.")
        return value