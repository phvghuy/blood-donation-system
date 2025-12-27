from django.urls import path
from src.presentation.views.blood_unit_view import BloodUnitListView

urlpatterns = [
    path('', BloodUnitListView.as_view(), name='list-blood-units'),
]