from django.db.models import Count
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from flowchart.models import Flowchart, Location, HistoryChange
from diagram.models import Block, Transition
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import FlowchartSerializer, LocationSerializer, HistoryChangeSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse
from django.db.models import Q
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
        return Response({'message': 'please select a location and a plan', 'error_code': 0, 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        primary_flowchart = Flowchart.objects.get(id=primary_flowchart_id, primary=True)
    except Flowchart.DoesNotExist:
        return Response({'message': 'Primary Flowchart Does not Exists', 'error_code': 1, 'error': True},
                        status=status.HTTP_404_NOT_FOUND)
    try:
        location_obj = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({'message': 'Location Does not Exists', 'error_code': 2, 'error': True},
                        status=status.HTTP_404_NOT_FOUND)

    flowchart, created = Flowchart.objects.get_or_create(name=primary_flowchart.name, location=location_obj)
    if not created:
        return Response({'message': 'This Flowchart Already Exists', 'error_code': 3,
                         'flowchart_id': flowchart.id, 'url': reverse('flowchart:flowchart_view', kwargs={'pk': flowchart.id}), 'error':  True},
                        status=status.HTTP_400_BAD_REQUEST)

    blocks = Block.objects.filter(flowchart=primary_flowchart).order_by('id')
    transitions = Transition.objects.filter((Q(start_block__in=blocks) | Q(end_block__in=blocks)))

    data = {}

    for block in blocks:
        block.pk = None
        block.is_approved = False
        block.is_active = False
        block.flowchart = flowchart
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
        transition.flowchart = flowchart
        transition.save()
    block = Block.objects.get(input_transition=None, flowchart_id=flowchart.id)
    block.is_active = True
    block.save()

    return Response({'message': 'new objects created', 'new_flowchart_id': flowchart.id, 'url': reverse('flowchart:flowchart_view', kwargs={'pk': flowchart.id})},
                    status=status.HTTP_201_CREATED)


@api_view(['Post'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def reset_flowchart(request):
    flowchart_id = request.data.get('flowchart_id')
    if not flowchart_id:
        return Response({'message': 'flowchart_name must be included', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        flowchart = Flowchart.objects.get(id=flowchart_id)
    except Flowchart.DoesNotExist:
        return Response({'message': 'flowchart does not exists', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)
    blocks = Block.objects.filter(flowchart__id=flowchart_id)
    for block in blocks:
        block.is_active = False
        block.is_approved = False
        block.is_pre_approved = False
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
    flowchart.is_active = False
    flowchart.save()
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
    if response.status_code == 200:
        block_history = json.loads(response.text)
    else:
        block_history = {}

    url = "http://127.0.0.1:8000/diagram/api/v1/comment-history/" + str(flowchart_id) + "/"
    response = requests.request("GET", url)
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
    try:
        if len(comment_history) > 0 or len(block_history) > 0:
            h = HistoryChange(flowchart=flowchart, comment_history=comment_history, block_history=block_history,
                              initial_date=flowchart.triggered_date)
            h.save()

        flowchart.is_active = False
        flowchart.triggered_date = None
        flowchart.save()

        response = requests.request("POST", url, headers=headers, data=payload)

        return Response({"message": "ok"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistoryChangeViewSet(viewsets.ModelViewSet):
    serializer_class = HistoryChangeSerializer
    queryset = HistoryChange.objects.all()


def f_create(flowchart_id, location_id):

    if flowchart_id == "0" or location_id == "0":
        return Response({'message': 'please select a location and a plan', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        primary_flowchart = Flowchart.objects.get(id=flowchart_id, primary=True)
    except Flowchart.DoesNotExist:
        return Response({'message': 'Primary Flowchart Does not Exists', 'error': True},
                        status=status.HTTP_404_NOT_FOUND)
    try:
        location_obj = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({'message': 'Location Does not Exists', 'error': True},
                        status=status.HTTP_404_NOT_FOUND)
    try:
        f = Flowchart.objects.filter(name=primary_flowchart.name, location=location_obj)
        return Response({'message': 'This Flowchart Already Exists', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)
    except Flowchart.DoesNotExist:
        pass

    new_flowchart = Flowchart.objects.create(name=primary_flowchart.name, location=location_obj)
    blocks = Block.objects.filter(flowchart=primary_flowchart).order_by('id')
    transitions = Transition.objects.filter((Q(start_block__in=blocks) | Q(end_block__in=blocks)))

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


def f_reset(flowchart_id):

    try:
        flowchart = Flowchart.objects.get(id=flowchart_id)
    except Flowchart.DoesNotExist:
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
    flowchart.is_active = False
    flowchart.save()
    return Response({'message': 'Flowchart rested successfully', 'error': False}, status=status.HTTP_200_OK)


def f_end(flowchart_id):

    try:
        flowchart = Flowchart.objects.get(id=flowchart_id)
    except Flowchart.DoesNotExist:
        return Response({'message': 'flowchart does not exists', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)

    url = "http://127.0.0.1:8000/diagram/api/v1/block-history/" + str(flowchart_id) + "/"
    response = requests.request("GET", url)
    if response.status_code == 200:
        block_history = json.loads(response.text)
    else:
        block_history = {}

    url = "http://127.0.0.1:8000/diagram/api/v1/comment-history/" + str(flowchart_id) + "/"
    response = requests.request("GET", url)
    if response.status_code == 200:
        comment_history = json.loads(response.text)
    else:
        comment_history = {}

    try:
        if len(comment_history) > 0 or len(block_history) > 0:
            h = HistoryChange(flowchart=flowchart, comment_history=comment_history, block_history=block_history,
                              initial_date=flowchart.triggered_date)
            h.save()

        flowchart.is_active = False
        flowchart.save()

        f_reset(flowchart_id)

        return Response({"message": "ok"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['Post'])
def ff(request):

    flowchart_id = request.data.get('flowchart_id')
    location_id = request.data.get('location_id')
    task = request.data.get('task')

    if not flowchart_id:
        return Response({"message": "No flowchart Id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        flowchart = Flowchart.objects.get(id=flowchart_id)
    except Flowchart.DoesNotExist:
        return Response({"message": "Invalid flowchart id"}, status=status.HTTP_400_BAD_REQUEST)

    if task == 'create':
        return f_create(flowchart_id, location_id)
    elif task == 'reset':
        return f_reset(flowchart_id)
    elif task == 'end':
        return f_end(flowchart_id)
