from django.urls import path, include
from . import views

urlpatterns = [
    path('members/', views.MemberViewSet.as_view({'get':"list"}), name='members'),
    path('send-custom-sms/', views.send_sms_api, name='send-custom-sms'),
    path('send-custom-email/', views.send_email_api, name='send-custom-email'),
    path('send-msg/', views.send_msg, name='send-smg')

    ]
