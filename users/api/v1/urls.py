from django.urls import path, include
from . import views

urlpatterns = [
    path('send-custom-sms/', views.send_sms_api, name='send-custom-sms'),
    path('send-custom-email/', views.send_email_api, name='send-custom-email'),

    ]
