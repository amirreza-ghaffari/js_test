from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('contacts/', views.ContactListView.as_view(), name='contacts'),
    path('mail_response_view/<str:random_text>/', views.mail_response_view, name='mail_response_view'),
    path('sms-panel/', views.sms_panel_view, name='sms-panel'),
    path('save_member_session/<str:member_id>/', views.save_member_session, name='save_member_session'),
    path('api/v1/', include('users.api.v1.urls')),
    path('', include('django.contrib.auth.urls')),

]
