from django.urls import path
from . import views

urlpatterns = [
    path('<str:name>/', views.flowchart_view, name='flowchart_view'),
]