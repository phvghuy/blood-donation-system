from django.db import models
from .hospital_model import HospitalModel
from .blood_type_model import BloodTypeModel

class BloodRequestModel(models.Model):
    STATUS_CHOICES = [
        ("pending", "Chờ duyệt"),
        ("approved", "Đẫ duyệt"),
        ("rejected", "Từ chối"),
        ("completed", "Hoàn tất"),
    ]

    hospital = models.ForeignKey(
        HospitalModel, on_delete=models.CASCADE
    )
    blood_type = models.ForeignKey(
        BloodTypeModel, on_delete=models.SET_NULL, null=True
    )
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    request_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "infrastructure_app"
        db_table = "blood_request"
