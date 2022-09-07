from django.urls import path, include
from . import views

from django.contrib.auth import urls
app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('contacts/', views.ContactListView.as_view(), name='contacts'),
    path('mail_response_view/<str:random_text>/', views.mail_response_view, name='mail_response_view'),
    path('', include('django.contrib.auth.urls')),
]
