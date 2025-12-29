from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from src.infrastructure.orm.blood_unit_model import BloodUnitModel
from src.infrastructure.serializers.blood_unit_serializer import (
    BloodUnitResponseSerializer,
    BloodUnitUpdateSerializer
)
from src.presentation.permissions import IsHospital, IsAdmin

# 1. View Lấy danh sách
class BloodUnitListView(generics.ListAPIView):
    """
    API lấy danh sách các đơn vị máu.
    Sử dụng ResponseSerializer để hiển thị thông tin chi tiết.
    """
    serializer_class = BloodUnitResponseSerializer
    permission_classes = [IsAuthenticated, IsHospital | IsAdmin]

    def get_queryset(self):
        return BloodUnitModel.objects.all().select_related('donor', 'blood_type').order_by('expiry_date')

# 2. View Cập nhật trạng thái
class BloodUnitStatusUpdateView(generics.UpdateAPIView):
    """
    API cập nhật trạng thái đơn vị máu.
    Chỉ cho phép phương thức PATCH.
    Sử dụng UpdateSerializer để chỉ cho phép sửa field 'status'.
    """
    queryset = BloodUnitModel.objects.all()
    serializer_class = BloodUnitUpdateSerializer
    permission_classes = [IsAuthenticated, IsHospital | IsAdmin]
    http_method_names = ['patch']
