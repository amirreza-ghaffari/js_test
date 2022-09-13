from django.urls import path
from . import views


urlpatterns = [
    path('flowcharts/', views.FlowchartViewSet.as_view({'get': 'list'}), name='flowchart-list'),
    path('locations/', views.LocationViewSet.as_view({'get': 'list'}), name='location-list'),


    path('incident_per_location/', views.incident_per_location, name='incident_per_location'),

    path('reset-flowchart/', views.reset_flowchart, name='reset-flowchart'),


    # ----------New Flowchart -------
    path('new-flowchart/', views.new_flowchart, name='new-flowchart'),
]