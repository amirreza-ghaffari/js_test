from django.urls import path, include
from django.contrib.auth import urls


app_name = "diagram"

urlpatterns = [
    path('api/v1/', include('diagram.api.v1.urls')),

]


