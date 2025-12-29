from django.urls import path
from src.presentation.views.request_view import HospitalRequestView, AdminRequestView

urlpatterns = [
    path('hospital/requests/', HospitalRequestView.as_view(), name='hospital-requests'),
    path('admin/requests/', AdminRequestView.as_view(), name='admin-requests-pending'),
    path('admin/requests/<int:pk>/', AdminRequestView.as_view(), name='admin-process-request'),
]