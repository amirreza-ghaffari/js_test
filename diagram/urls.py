from django.urls import path, include
from django.contrib.auth import urls
from .views import approved_block


app_name = "diagram"

urlpatterns = [
    path('api/v1/', include('diagram.api.v1.urls')),
    path('approve_block/<str:block_label>/', approved_block, name='approve_block'),

]


