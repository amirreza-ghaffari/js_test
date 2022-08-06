from django.urls import path, include
from .views import login_view, profile_view, create_user_view

from django.contrib.auth import urls


urlpatterns = [
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('add_user/',  create_user_view, name='add_user'),
    path('', include('django.contrib.auth.urls')),

]
