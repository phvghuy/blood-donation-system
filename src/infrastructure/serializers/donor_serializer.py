from rest_framework import serializers

class DonorResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    full_name = serializers.CharField()
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    blood_type_id = serializers.IntegerField()

class CreateDonorRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    full_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    gender = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    blood_type_id = serializers.IntegerField()