from django.db import models
from django.contrib.auth.models import User
from .blood_type_model import BloodTypeModel

class DonorModel(models.Model):
    GENDER_CHOICES = [
        ("male", "Nam"),
        ("female", "Nữ"),
        ("other", "Khác"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="donor_profile"
    )
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    blood_type = models.ForeignKey(
        BloodTypeModel, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "infrastructure_app"
        db_table = "donor"

    def __str__(self):
        return self.full_name
