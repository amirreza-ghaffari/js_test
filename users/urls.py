from django.urls import path, include
from .views import login_view

from django.contrib.auth import urls
app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', include('django.contrib.auth.urls')),

]
