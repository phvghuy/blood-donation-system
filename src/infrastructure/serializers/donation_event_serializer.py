from rest_framework import serializers
from datetime import date
from src.infrastructure.orm.blood_type_model import BloodTypeModel

class CreateDonationEventSerializer(serializers.Serializer):
    donor_id = serializers.IntegerField(help_text="ID của người hiến máu")
    blood_type = serializers.CharField(max_length=3, help_text="Tên của nhóm máu")
    donation_date = serializers.DateField(help_text="Ngày hiến máu")
    location = serializers.CharField(required=False, allow_blank=True)

    def validate_donation_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Ngày hiến máu không hợp lệ (ngày hiến máu không được ở tương lai).")
        return value

    def validate_blood_type(self, value):
        if not BloodTypeModel.objects.filter(type_name=value).exists():
            raise serializers.ValidationError("Nhóm máu không tồn tại.")
        return value