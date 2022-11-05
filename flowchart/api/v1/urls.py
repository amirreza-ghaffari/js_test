from django.urls import path
from . import views


urlpatterns = [
    path('flowcharts/', views.FlowchartViewSet.as_view({'get': 'list'}), name='flowchart-list'),
    path('flowcharts/<str:pk>/', views.FlowchartViewSet.as_view({'get': 'retrieve'}), name='flowchart-list'),
    path('locations/', views.LocationViewSet.as_view({'get': 'list'}), name='location-list'),
    path('contingency-plans/', views.ContingencyPlanViewSet.as_view({'get': 'list'}), name='contingency-plans'),

    # ------------------------------------------- Charts ---------------------------------
    path('incident_per_location/', views.incident_per_location, name='incident_per_location'),
    path('total_incident/', views.total_incident, name='total_incident'),
    path('incident_per_contingency/', views.incident_per_contingency, name='incident_per_contingency'),

    # ---------------------------------- FlowCharts ----------------------------------------
    path('reset-flowchart/', views.reset_flowchart, name='reset-flowchart'),


    # ----------New Flowchart -------
    path('new-flowchart/', views.new_flowchart, name='new-flowchart'),

    # ----------End Flowchart --------
    path('end-incident/', views.end_incident, name='End-Incident'),

    path('HistoryChange/<str:pk>/', views.HistoryChangeViewSet.as_view({'get': 'retrieve'}), name='history-change-detail'),

    path('ff/', views.ff , name='ff'),

]