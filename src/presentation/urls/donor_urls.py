from django.urls import path
from src.presentation.views.donor_views import (
    DonorRegisterView,
    DonorLoginView,
    DonorProfileView,
    DonorDetailView
)

urlpatterns = [
    path('donors/register/', DonorRegisterView.as_view(), name='donor-register'),
    path('donors/login/', DonorLoginView.as_view(), name='donor-login'),
    path('donors/profile/', DonorProfileView.as_view(), name='donor-profile'),
    path('donors/<int:pk>/', DonorDetailView.as_view(), name='donor-detail'),
]

