from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/v1/blocks/', views.block_list, name='block_list'),
    path('api/v1/transitions/', views.transition_list, name='transition_list'),
    ]