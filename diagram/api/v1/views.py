import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ...models import Block, Transition
from .serializers import BlockSerializer, TransitionSerializer


@api_view(['GET'])
def block_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        blocks = Block.objects.all()
        serializer = BlockSerializer(blocks, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def transition_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        transitions = Transition.objects.all()
        serializer = TransitionSerializer(transitions, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def full_list(request):
    if request.method == 'GET':
        a = {"class": "GraphLinksModel"}

        blocks = Block.objects.all()
        serializer = BlockSerializer(blocks, many=True)
        a["nodeDataArray"] = serializer.data

        transitions = Transition.objects.all()
        serializer = TransitionSerializer(transitions, many=True)
        a["linkDataArray"] = serializer.data

        return Response(json.dumps(a))









