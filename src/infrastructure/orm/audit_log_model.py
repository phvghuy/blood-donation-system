from django.db import models
from django.contrib.auth.models import User

class AuditLogModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    action = models.TextField()
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "infrastructure_app"
        db_table = "audit_log"
