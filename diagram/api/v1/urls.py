from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework import routers


urlpatterns = [
    path('blocks/', views.BlockViewSet.as_view({'get': 'list', 'post': 'create'}), name='block-list'),
    path('blocks/<str:pk>/', views.BlockViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='block-detail'),

    path('transitions/', views.TransitionViewSet.as_view({'get': 'list', 'post': 'create'}), name='transition-list'),
    path('transitions/<str:pk>/', views.TransitionViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='transition-detail'),

    # ----------- History ----------

    path('history/', views.history_api, name='history'),
    path('his/', views.his, name='history'),

    path('history_diff/<str:pk>/', views.HistoryChangeView.as_view({'get': 'retrieve'}), name='his_diff'),

    # ----------New Flowchart -------
    path('new_flowchart/<str:old_flowchart_name>/<str:new_flowchart_name>/', views.new_flowchart, name='new_flowchart')


    ]
