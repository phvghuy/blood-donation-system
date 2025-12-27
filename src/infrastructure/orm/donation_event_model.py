from django.db import models
from .donor_model import DonorModel
from .blood_unit_model import BloodUnitModel

class DonationEventModel(models.Model):
    donor = models.ForeignKey(
        DonorModel, on_delete=models.CASCADE
    )
    blood_unit = models.OneToOneField(
        BloodUnitModel, on_delete=models.CASCADE
    )
    event_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200, blank=True)

    class Meta:
        app_label = "infrastructure_app"
        db_table = "donation_event"
