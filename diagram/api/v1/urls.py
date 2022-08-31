from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework import routers


urlpatterns = [
    path('blocks/', views.BlockViewSet.as_view({'get': 'list', 'post': 'create'}), name='block-list'),
    path('blocks/<str:pk>/', views.BlockViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='block-detail'),

    path('transitions/', views.TransitionViewSet.as_view({'get': 'list', 'post': 'create'}), name='transition-list'),
    path('transitions/<str:pk>/', views.TransitionViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='transition-detail'),

    path('active_blocks/<str:flowchart_id>/', views.active_blocks, name='active-blocks'),
    path('active_transitions/<str:flowchart_id>/', views.active_transitions, name='active-transients'),



    # ----------- History ----------

    path('history/', views.history_api, name='history'),
    path('his/', views.his, name='history'),

    path('history_diff/<str:pk>/', views.HistoryChangeView.as_view({'get': 'retrieve'}), name='his_diff'),



    path('test/', views.test, name='test'),


    # ---------- Comment -----------
    path('comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
    path('comments/<str:pk>/', views.CommentViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update',
                                                             'delete': 'destroy'}), name='comment-detail'),


    ]
