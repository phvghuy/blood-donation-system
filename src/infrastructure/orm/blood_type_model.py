from django.db import models

class BloodTypeModel(models.Model):
    type_name = models.CharField(max_length=10, unique=True)

    class Meta:
        app_label = "infrastructure_app"
        db_table = "blood_type"

    def __str__(self):
        return self.type_name
