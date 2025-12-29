from django.urls import path
from src.presentation.views.donation_event_view import CreateDonationEventView

urlpatterns = [
    path('', CreateDonationEventView.as_view(), name='create-donation-event'),
]