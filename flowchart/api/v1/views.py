from flowchart.models import Flowchart
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



