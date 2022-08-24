from django.urls import path
from . import views


urlpatterns = [
    path('flowcharts/', views.FlowchartViewSet.as_view({'get': 'list'}), name='flowchart-list'),

    # ----------New Flowchart -------
    # path('new_flowchart/<str:old_flowchart_name>/<str:new_flowchart_name>/', views.new_flowchart, name='new_flowchart'),
]