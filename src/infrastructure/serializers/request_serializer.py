from rest_framework import serializers

class CreateRequestSerializer(serializers.Serializer):
    blood_type_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class ProcessRequestSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['approved', 'rejected'])

class RequestResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    hospital_name = serializers.CharField()
    blood_type_name = serializers.CharField()
    quantity = serializers.IntegerField()
    status = serializers.CharField()
    request_date = serializers.DateTimeField()