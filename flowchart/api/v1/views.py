from django.db.models import Count, Q, Sum
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from flowchart.models import Flowchart, Location, HistoryChange
from diagram.models import Block, Transition
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import FlowchartSerializer, LocationSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse
import requests
import json


class FlowchartViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FlowchartSerializer
    queryset = Flowchart.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['primary', 'is_active']


class LocationViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


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


@api_view(['Post'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def new_flowchart(request):
    primary_flowchart_id = request.data.get('primary_id')
    location_id = request.data.get('location_id')

    if primary_flowchart_id == "0" or location_id == "0":
        return Response({'message': 'please select a location and a plan', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        primary_flowchart = Flowchart.objects.get(id=primary_flowchart_id, primary=True)
    except Flowchart.DoesNotExist:
        return Response({'message': 'Primary Flowchart Does not Exists', 'error': True},
                        status=status.HTTP_404_NOT_FOUND)
    try:
        location_obj = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({'message': 'Location Does not Exists', 'error': True},
                        status=status.HTTP_404_NOT_FOUND)
    if Flowchart.objects.filter(name=primary_flowchart.name, location=location_obj).exists():
        return Response({'message': 'This Flowchart Already Exists', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)

    new_flowchart = Flowchart.objects.create(name=primary_flowchart.name, location=location_obj)
    blocks = Block.objects.filter(flowchart=primary_flowchart)
    transitions = Transition.objects.filter(flowchart=primary_flowchart)

    data = {}

    for block in blocks:
        block.pk = None
        block.is_approved = False
        block.is_active = False
        block.flowchart = new_flowchart
        block.save()
        data[block.label] = block.id

    for transition in transitions:
        transition.pk = None
        transition.is_active = False
        transition.is_approved = False
        start_block_name = transition.start_block.label
        end_block_name = transition.end_block.label
        transition.start_block_id = data[start_block_name]
        transition.end_block_id = data[end_block_name]
        transition.flowchart = new_flowchart
        transition.save()
    block = Block.objects.get(input_transition=None, flowchart_id=new_flowchart.id)
    block.is_active = True
    block.save()

    return Response({'message': 'new objects created', 'new_flowchart_id': new_flowchart.id, 'url': reverse('flowchart:flowchart_view', kwargs={'pk': new_flowchart.id})},
                    status=status.HTTP_201_CREATED)


@api_view(['Post'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def reset_flowchart(request):
    flowchart_id = request.data.get('flowchart_id')
    if not flowchart_id:
        return Response({'message': 'flowchart_name must be included', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)

    if not Flowchart.objects.filter(id=flowchart_id).exists():
        return Response({'message': 'flowchart does not exists', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)
    blocks = Block.objects.filter(flowchart__id=flowchart_id)
    for block in blocks:
        block.is_active = False
        block.is_approved = False
        block.block_comment.all().delete()
        block.save()

    b = Block.objects.get(flowchart__id=flowchart_id, input_transition=None)
    b.is_active = True
    b.save()
    transitions = Transition.objects.filter(flowchart__id=flowchart_id)
    for tr in transitions:
        tr.is_approved = False
        tr.is_active = False
        tr.save()
    return Response({'message': 'Flowchart rested successfully', 'error': False}, status=status.HTTP_200_OK)

@api_view(['Post'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def end_incident(request):

    flowchart_id = request.data.get('flowchart_id')
    if not flowchart_id:
        return Response({'message': 'flowchart_id must be included', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        flowchart = Flowchart.objects.get(id=flowchart_id)
    except Flowchart.DoesNotExist:
        return Response({'message': 'flowchart does not exists', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)

    url = "http://127.0.0.1:8000/diagram/api/v1/block-history/" + str(flowchart_id) + "/"
    response = requests.request("GET", url)
    print(response.text)
    if response.status_code == 200:
        block_history = json.loads(response.text)
    else:
        block_history = {}

    url = "http://127.0.0.1:8000/diagram/api/v1/comment-history/" + str(flowchart_id) + "/"
    response = requests.request("GET", url)
    print(response.text)
    if response.status_code == 200:
        comment_history = json.loads(response.text)
    else:
        comment_history = {}

    url = "http://127.0.0.1:8000/flowchart/api/v1/reset-flowchart/"
    payload = json.dumps({
        "flowchart_id": flowchart_id
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    h = HistoryChange(flowchart=flowchart, comment_history=comment_history, block_history=block_history,
                      initial_date=flowchart.updated_date)
    h.save()

    return Response({"message": "ok"}, status=status.HTTP_200_OK)
