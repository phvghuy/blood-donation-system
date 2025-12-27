from django.contrib import admin
from src.infrastructure.orm.blood_type_model import BloodTypeModel
from src.infrastructure.orm.donor_model import DonorModel
from src.infrastructure.orm.hospital_model import HospitalModel
from src.infrastructure.orm.blood_unit_model import BloodUnitModel
from src.infrastructure.orm.donation_event_model import DonationEventModel
from src.infrastructure.orm.request_model import BloodRequestModel
from src.infrastructure.orm.audit_log_model import AuditLogModel

admin.site.register(BloodTypeModel)
admin.site.register(DonorModel)
admin.site.register(HospitalModel)
admin.site.register(BloodUnitModel)
admin.site.register(DonationEventModel)
admin.site.register(BloodRequestModel)
admin.site.register(AuditLogModel)
