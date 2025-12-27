from django.urls import path
from src.presentation.views.blood_type_views import (
    BloodTypeListCreateView,
    BloodTypeDetailView,
    BloodTypeInitializeView
)

urlpatterns = [
    path('blood-types/', BloodTypeListCreateView.as_view(), name='blood-type-list-create'),
    path('blood-types/<int:pk>/', BloodTypeDetailView.as_view(), name='blood-type-detail'),
    path('blood-types/initialize/', BloodTypeInitializeView.as_view(), name='blood-type-initialize'),
]

