from django.urls import path, include
from . import views

urlpatterns = [
    path('send-custom-sms/', views.sens_sms_view, name='send-custom-sms'),
    ]
