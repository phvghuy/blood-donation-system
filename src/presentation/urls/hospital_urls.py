from django.urls import path
from src.presentation.views.hospital_view import HospitalListView, HospitalDetailView

urlpatterns = [
    path('hospitals/', HospitalListView.as_view(), name='hospital-list'),
    path('hospitals/<int:pk>/', HospitalDetailView.as_view(), name='hospital-detail'),
]