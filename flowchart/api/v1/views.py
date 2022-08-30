from django.db.models import Count, Q, Sum
from django.db.models.functions import Coalesce
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from flowchart.models import Flowchart, Location
from diagram.models import Block, Transition
from rest_framework import permissions, generics, viewsets
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import FlowchartSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class FlowchartViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = Flowchart.objects.all()
        serializer = FlowchartSerializer(queryset, many=True)
        return Response(serializer.data)


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


def new_flowchart(request, old_flowchart_name, new_flowchart_name):

    try:
        old_flowchart_obj = Flowchart.objects.get(name=old_flowchart_name)
    except Flowchart.DoesNotExist:
        return Response({'error': 'old flowchart does not exists'}, status=status.HTTP_404_NOT_FOUND)

    try:
        new_flowchart_obj = Flowchart.objects.get(name=new_flowchart_name)
    except Flowchart.DoesNotExist:
        return Response({'error': 'new flowchart does not exists'}, status=status.HTTP_404_NOT_FOUND)
    blocks = Block.objects.filter(flowchart=old_flowchart_obj)
    transitions = Transition.objects.filter(flowchart=old_flowchart_obj)

    for block in blocks:
        block.pk = None
        block.is_approved = False
        block.is_active = False
        block.flowchart = new_flowchart_obj
        block.save()

    for transition in transitions:
        transition.pk = None
        transition.is_active = False
        transition.is_approved = False
        transition.flowchart = new_flowchart_obj
        transition.save()

    return Response({'detail': 'new objects created'}, status=status.HTTP_201_CREATED)



