from django.urls import path, include
from . import views

app_name = "flowchart"


urlpatterns = [
    path('api/v1/', include('flowchart.api.v1.urls')),
    path('view/<str:pk>/', views.flowchart_view, name='flowchart_view'),
    path('history-dashboard/', views.history_list, name='history-list'),
    path('history/<str:pk>/', views.history_detail, name='history-detail'),

]