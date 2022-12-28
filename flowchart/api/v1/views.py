from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from flowchart.models import Flowchart, Location, HistoryChange, ContingencyPlan
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import FlowchartSerializer, LocationSerializer, HistoryChangeSerializer, ContingencyPlanSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from flowchart.utils import f_reset, f_end, f_create


class FlowchartViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FlowchartSerializer
    queryset = Flowchart.objects.all().order_by('-is_active')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['primary', 'is_active']


class LocationViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class ContingencyPlanViewSet(viewsets.ModelViewSet):
    serializer_class = ContingencyPlanSerializer
    queryset = ContingencyPlan.objects.all()


@api_view(['Get'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def incident_per_location(request):
    active_incidents = Location.objects.values('name').annotate(total=Count('flowchart')).order_by('name')

    closed_incident = Location.objects.values('name', 'incident_number').order_by('name')

    data = {}
    for obj1, obj2 in zip(closed_incident, active_incidents):
        data[obj1['name']] = {'closed': obj1['incident_number'], 'active': obj2['total']}

    return Response(data)


class HistoryChangeViewSet(viewsets.ModelViewSet):
    serializer_class = HistoryChangeSerializer
    queryset = HistoryChange.objects.all()


@api_view(['Post'])
def flowchart_utility(request):

    flowchart_id = request.data.get('flowchart_id')
    location_id = request.data.get('location_id')
    task = request.data.get('task')

    if not flowchart_id:
        return Response({"message": "No flowchart Id provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        flowchart = Flowchart.objects.get(id=flowchart_id)
    except Flowchart.DoesNotExist:
        return Response({"message": "Invalid flowchart id"}, status=status.HTTP_400_BAD_REQUEST)

    if task == 'create':
        return f_create(flowchart_id, location_id)
    elif task == 'reset':
        return f_reset(flowchart_id)
    elif task == 'end':
        return f_end(flowchart_id, request)


@api_view(['Get'])
def incident_per_location(request):
    temp = {}
    opened = []
    queryset = Flowchart.objects.all()
    locs = queryset.exclude(location=None).values('location__name').annotate(count=Sum('incident_counter')).order_by('location__name')
    temp['names'] = locs.values_list('location__name', flat=True)
    temp['closed'] = locs.values_list('count', flat=True)
    for loc_name in temp['names']:
        opens = queryset.filter(is_active=True, location__name=loc_name).values('location__name').annotate(count=Count('is_active'))
        if len(opens) == 0:
            opened.append(0)
        else:
            opened.append(opens[0]['count'])

    temp['opened'] = opened
    return Response(temp, status=status.HTTP_200_OK)


@api_view(['Get'])
def total_incident(request):
    temp = {}
    queryset = Flowchart.objects.all()
    closed = queryset.values('incident_counter').aggregate(count=Sum('incident_counter'))['count']
    opened = queryset.filter(is_active=True).count()
    temp['closed'] = closed
    temp['open'] = opened
    return Response(temp, status=status.HTTP_200_OK)


@api_view(['Get'])
def incident_per_contingency(request):
    temp = {}
    counts = []
    names = []
    flowchart_names = list(Flowchart.objects.filter(primary=True).values_list('name', flat=True).order_by('name'))
    for name in flowchart_names:
        c = Flowchart.objects.filter(primary=False, name__contains=name).values('incident_counter').aggregate(count=Sum('incident_counter'))['count']
        counts.append(c)
        names.append(name)
    temp['names'] = names
    temp['counts'] = counts
    return Response(temp, status=status.HTTP_200_OK)


@api_view(['Get'])
def incident_per_month(request):
    temp = {}
    months = []
    counts = []
    histories = HistoryChange.objects.annotate(month=TruncMonth('j_initial_date')).values('month').annotate(count=Count('id')).values('month', 'count')
    for item in histories:
        months.append('-'.join(str(item['month']).split('-')[0:2]))
        counts.append(item['count'])
    temp['months'] = months
    temp['counts'] = counts
    return Response(temp, status=status.HTTP_200_OK)
