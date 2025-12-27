from rest_framework import generics
from src.infrastructure.orm.blood_unit_model import BloodUnitModel
from src.infrastructure.serializers.blood_unit_serializer import BloodUnitSerializer


class BloodUnitListView(generics.ListAPIView):
    serializer_class = BloodUnitSerializer

    def get_queryset(self):
        return BloodUnitModel.objects.filter(
            status='available'
        ).order_by('expiry_date')