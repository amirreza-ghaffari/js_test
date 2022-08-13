import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

from ...models import Block, Transition
from .serializers import BlockSerializer, TransitionSerializer, HistorySerializer, CustomerHistorySerializer


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

#TODO: change it to POST method
@api_view(['GET'])
def approve_block_api(request, block_label):

    user = request.user
    try:
        start_block = Block.objects.get(label=block_label)
    except Block.DoesNotExist:
        return JsonResponse({'error': f'This block with label "{block_label}" does not exists'})

    if start_block.user_groups and user not in start_block.user_groups.user_set.all():
        return JsonResponse({'error': f'The user "{user}" does not have permission to "{block_label}"!'})

    if start_block.active:

        start_block_group = start_block.group
        start_block.is_approved = True
        start_block.is_active = False
        start_block.color = 'green'
        start_block.save()

        group_approved_flag = True

        for block_obj in Block.objects.filter(group=start_block_group).all():
            if block_obj.is_approved is False and block_obj.group:
                group_approved_flag = False

        try:
            transients = Transition.objects.filter(start_block=start_block)
            for transient_obj in transients:
                end_block = transient_obj.end_block

                if (end_block.group and end_block.group == start_block_group) or (start_block_group is None) or (group_approved_flag):
                    transient_obj.is_active = True
                    transient_obj.save()
                    #  send email or sms or print in terminal #
                    end_block.is_active = True
                    end_block.color = 'red'
                    end_block.save()

        except Transition.DoesNotExist:
            return JsonResponse(
                {'error': f'This block {start_block} does not has transient'})
        return JsonResponse({'detail': f'Block with id "{start_block.id}" and label "{start_block.label}" approved successfully'})
    else:
        return JsonResponse({'error': f'This block with id "{start_block.id}" and label "{start_block.label}" has not been activated yet'})


@api_view(['GET'])
def history_api(request):

    blocks = Block.objects.all()
    serializer = HistorySerializer(blocks, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def his(request):
    serializer = CustomerHistorySerializer(Block.history.all().order_by('-history_date').filter(Q(approved=True) | Q(active=True)), many=True, read_only=True)
    return Response(serializer.data)


class TransitionPartialUpdateView(GenericAPIView, UpdateModelMixin):
    '''
    You just need to provide the field which is to be modified.
    '''
    queryset = Transition.objects.all()
    serializer_class = TransitionSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class BlockPartialUpdateView(GenericAPIView, UpdateModelMixin):

    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)