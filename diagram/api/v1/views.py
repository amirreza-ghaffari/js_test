from flowchart.models import Flowchart
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import permissions, generics
from ...models import Block, Transition
from .serializers import BlockSerializer, TransitionSerializer, HistorySerializer, CustomerHistorySerializer, Custom2
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class CustomPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        groups = obj.user_groups.all()
        if user.is_staff or user.is_superuser:
            return True
        for group in groups:
            if user in group.user_set.all():
                return True
        return False


class BlockViewSet(ModelViewSet):

    permission_classes = [CustomPermission]
    serializer_class = BlockSerializer
    queryset = Block.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['flowchart', 'is_approved', 'is_active']


class TransitionViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['flowchart', 'is_approved', 'is_active']

    permission_classes = [IsAuthenticated]
    serializer_class = TransitionSerializer
    queryset = Transition.objects.all()


@api_view(['GET'])
def history_api(request):

    blocks = Block.objects.all()
    serializer = HistorySerializer(blocks, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def his(request):
    serializer = CustomerHistorySerializer(Block.history.all().order_by('-history_date').filter(Q(is_approved=True) | Q(is_active=True)), many=True, read_only=True)
    return Response(serializer.data)


class HistoryChangeView(ViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = Custom2
    queryset = Block.objects.all()

    def retrieve(self, request, pk=None):
        block = get_object_or_404(self.queryset, pk=pk)
        histories = block.history.all()
        if len(histories) > 1:
            new_record, old_record = block.history.all()[0:2]
            delta = new_record.diff_against(old_record, included_fields=['is_approved', 'is_active', 'label'])
            serializer = self.serializer_class(delta.changes, many=True)
            data = serializer.data
            user = new_record.history_user.full_name
            change_date = new_record.history_date
            z = {'changes': data, 'user': user, 'change_date': naturaltime(change_date)}
            return Response(z, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'this object has no history change'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def new_flowchart(request, old_flowchart_name, new_flowchart_name):

    try:
        old_flowchart_obj = Flowchart.objects.get(name=old_flowchart_name)
    except Flowchart.DoesNotExist:
        return Response({'error': 'flowchart does not exists'}, status=status.HTTP_404_NOT_FOUND)

    try:
        new_flowchart_obj = Flowchart.objects.get(name=new_flowchart_name)
    except Flowchart.DoesNotExist:
        return Response({'error': 'flowchart does not exists'}, status=status.HTTP_404_NOT_FOUND)
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