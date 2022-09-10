from django.db.models import Count, Q, Sum
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from flowchart.models import Flowchart, Location
from diagram.models import Block, Transition
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import FlowchartSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend


class FlowchartViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FlowchartSerializer
    queryset = Flowchart.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['primary', 'is_active']


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
@permission_classes([IsAuthenticated])
def new_flowchart(request, primary_name, location_name):

    try:
        primary_flowchart = Flowchart.objects.get(name=primary_name, primary=True)
    except Flowchart.DoesNotExist:
        return Response({'message': 'Primary Flowchart Does not Exists', 'error': True},
                        status=status.HTTP_404_NOT_FOUND)
    try:
        location_obj = Location.objects.get(name=location_name)
    except Location.DoesNotExist:
        return Response({'message': 'Location Does not Exists', 'error': True},
                        status=status.HTTP_404_NOT_FOUND)
    if Flowchart.objects.filter(name=primary_flowchart.name, location=location_obj):
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
    block = Block.objects.get(label='شروع', flowchart_id=new_flowchart.id)
    block.is_active = True
    block.save()

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

    return Response({'message': 'new objects created', 'new_flowchart_id': new_flowchart.id},
                    status=status.HTTP_201_CREATED)


@api_view(['Post'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def reset_flowchart(request):
    flowchart_name = request.data.get('flowchart_name')
    if not flowchart_name:
        return Response({'message': 'flowchart_name must be included', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)

    if not Flowchart.objects.filter(name=flowchart_name).exists():
        return Response({'message': 'flowchart does not exists', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)
    blocks = Block.objects.filter(flowchart__name=flowchart_name)
    for block in blocks:
        block.is_active = False
        block.is_approved = False
        block.save()
    b = Block.objects.get(label='شروع', flowchart__name=flowchart_name)
    b.is_active = True
    b.save()
    transitions = Transition.objects.filter(flowchart__name=flowchart_name)
    for tr in transitions:
        tr.is_approved = False
        tr.is_active = False
        tr.save()
    return Response({'message': 'Flowchart rested successfully', 'error': False}, status=status.HTTP_200_OK)


