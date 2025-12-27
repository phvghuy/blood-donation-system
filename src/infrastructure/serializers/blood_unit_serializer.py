from rest_framework import serializers
from src.infrastructure.orm.blood_unit_model import BloodUnitModel

class BloodUnitSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    donor_name = serializers.CharField(source='donor.full_name', read_only=True)
    blood_type_display = serializers.CharField(source='get_blood_type_display', read_only=True)

    class Meta:
        model = BloodUnitModel
        fields = [
            'id',
            'donor_name',
            'blood_type_display',
            'donation_date',
            'expiry_date',
            'status_display',
            'created_at'
        ]