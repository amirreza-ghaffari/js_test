from django.urls import path
from . import views


urlpatterns = [
    path('flowcharts/', views.FlowchartViewSet.as_view({'get': 'list'}), name='flowchart-list'),
    path('flowcharts/<str:pk>/', views.FlowchartViewSet.as_view({'get': 'retrieve'}), name='flowchart-list'),
    path('locations/', views.LocationViewSet.as_view({'get': 'list'}), name='location-list'),

    # ------------------------------------------- Charts ---------------------------------
    path('incident_per_location/', views.incident_per_location, name='incident_per_location'),
    path('total_incident/', views.total_incident, name='total_incident'),
    path('incident_per_contingency/', views.incident_per_contingency, name='incident_per_contingency'),
    path('contingency-plans/', views.ContingencyPlanViewSet.as_view({'get': 'list'}), name='contingency-plans'),
    path('incident-per-month/', views.incident_per_month, name='incident-per-month'),

    # ---------------------------------- FlowCharts ----------------------------------------
    path('HistoryChange/<str:pk>/', views.HistoryChangeViewSet.as_view({'get': 'retrieve'}), name='history-change-detail'),
    path('flowchart-utility/', views.flowchart_utility, name='flowchart-utility'),

    # ---------------------------------- ScreenShot ----------------------------------------
    path('screenshot/', views.ScreenViewSet.as_view({'post': 'create'})),
    path('screenshot/<str:pk>/', views.ScreenViewSet.as_view({'get': 'retrieve'})),



]