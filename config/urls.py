"""
URL configuration for blood_donation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from src.presentation.urls.blood_type_urls import urlpatterns as blood_type_urls
from src.presentation.urls.donation_event_urls import urlpatterns as donation_event_urls
from src.presentation.urls.blood_unit_urls import urlpatterns as blood_unit_urls
from src.presentation.urls.auth_urls import urlpatterns as auth_urls
from src.presentation.urls.donor_urls import urlpatterns as donor_urls
from src.presentation.urls.hospital_urls import urlpatterns as hospital_urls
from src.presentation.urls.request_urls import urlpatterns as request_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/donation-events/', include(donation_event_urls)),
    path('api/blood-units/', include(blood_unit_urls)),
    path('api/auth/', include(auth_urls)),
    path('api/', include(donor_urls)),
    path('api/', include(hospital_urls)),
    path('api/', include(request_urls)),
]
