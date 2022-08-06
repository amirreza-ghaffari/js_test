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
        snippets = Block.objects.all()
        serializer = BlockSerializer(snippets, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def transition_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Transition.objects.all()
        serializer = TransitionSerializer(snippets, many=True)
        return Response(serializer.data)
