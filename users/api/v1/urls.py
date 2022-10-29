from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.MemberViewSet.as_view({'get': "list"}), name='members'),
    path('send-msg/', views.send_block_msg, name='send-smg'),
    path('custom-send-smg/', views.custom_send_smg, name='custom_send_smg'),
    ]
