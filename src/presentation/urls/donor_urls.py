from django.urls import path
from src.presentation.views.donor_view import DonorView, DonorDetailView

urlpatterns = [
    path('donors/', DonorView.as_view(), name='manage-donors'),
    path('donors/<int:pk>/', DonorDetailView.as_view(), name='donor-detail'),
]