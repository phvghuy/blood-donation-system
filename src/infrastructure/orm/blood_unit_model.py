from django.db import models
from .donor_model import DonorModel
from .blood_type_model import BloodTypeModel

class BloodUnitModel(models.Model):
    STATUS_CHOICES = [
        ("available", "Còn trong kho"),
        ("reserved", "Đã giữ cho yêu cầu"),
        ("used", "Đã sử dụng"),
        ("expired", "Hết hạn sử dụng"),
    ]

    donor = models.ForeignKey(
        DonorModel, on_delete=models.SET_NULL, null=True
    )
    blood_type = models.ForeignKey(
        BloodTypeModel, on_delete=models.CASCADE
    )
    donation_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "infrastructure_app"
        db_table = "blood_unit"

    def __str__(self):
        return f"BloodUnit #{self.id} - {self.blood_type}"
