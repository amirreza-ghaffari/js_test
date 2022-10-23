from django.urls import path, include
from . import views

urlpatterns = [
    path('members/', views.MemberViewSet.as_view({'get': "list"}), name='members'),
    path('send-msg/', views.send_msg, name='send-smg')

    ]
