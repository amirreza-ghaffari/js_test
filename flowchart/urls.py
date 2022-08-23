from django.urls import path, include
from . import views

app_name = "flowchart"


urlpatterns = [
    path('api/v1/', include('flowchart.api.v1.urls')),
    path('<str:name>/', views.flowchart_view, name='flowchart_view'),
]