from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers


urlpatterns = [
    path('api/v1/blocks/', views.block_list, name='block_list'),
    path('api/v1/transitions/', views.transition_list, name='transition_list'),
    path('api/v1/transitions_blocks/', views.full_list, name='full_data'),
    # path('api/v1/approve_block/<str:block_label>/', views.approve_block_api, name='approve_block_api'),
    path('api/v1/approve_block/<int:pk>/', views.BlockPartialUpdateView.as_view(), name='approve_block'),
    path('api/v1/approve_transition/<int:pk>/', views.TransitionPartialUpdateView.as_view(), name='approve_transition'),
    path('api/v1/history/', views.history_api, name='history'),
    path('api/v1/his/', views.his, name='history'),
    ]
