from django.urls import path, include
from django.contrib.auth import urls
from . import views


app_name = "diagram"

urlpatterns = [
    path('api/v1/', include('diagram.api.v1.urls')),
    path('block_info/<str:pk>/', views.block_info_view, name='block_info'),

]


