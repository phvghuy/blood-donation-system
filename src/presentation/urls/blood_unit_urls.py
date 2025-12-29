from django.urls import path
from src.presentation.views.blood_unit_view import BloodUnitListView
from src.presentation.views.blood_unit_view import BloodUnitStatusUpdateView

urlpatterns = [
    path('', BloodUnitListView.as_view(), name='list-blood-units'),
    path('<int:pk>/', BloodUnitStatusUpdateView.as_view(), name='update-blood-unit-status'),
]