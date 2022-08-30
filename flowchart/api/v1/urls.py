from django.urls import path
from . import views


urlpatterns = [
    path('flowcharts/', views.FlowchartViewSet.as_view({'get': 'list'}), name='flowchart-list'),


    path('incident_per_location/', views.incident_per_location, name='incident_per_location'),




    # ----------New Flowchart -------
    # path('new_flowchart/<str:old_flowchart_name>/<str:new_flowchart_name>/', views.new_flowchart, name='new_flowchart'),
]