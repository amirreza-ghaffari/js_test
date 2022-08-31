from flowchart.models import Flowchart
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import permissions, generics
from ...models import Block, Transition, Comment
from .serializers import BlockSerializer, TransitionSerializer, HistorySerializer, CustomerHistorySerializer, Custom2, CommentSerializer
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


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

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def active_blocks(request, flowchart_id):
    blocks = Block.objects.filter(is_active=True, flowchart_id=flowchart_id)
    serializer = BlockSerializer(blocks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def active_transitions(request, flowchart_id):
    transient = Transition.objects.filter(is_active=True, flowchart_id=flowchart_id)
    serializer = TransitionSerializer(transient, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def active_transition(request):
#     transition = Transition.objects.get(is_active=True)
#     return Response({'data': {'height': block.loc_height, 'length': block.loc_length}}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test(request):
     return Response({'x': [10,11,2,7], 'y': [20,4,7,10], 'z': [4,1,8,12]})


class CommentViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('-updated_date')
    # def get_queryset(self):
    #     flowchart_id = self.request.GET.get('flowchart_id')
    #     if flowchart_id:
    #         return Comment.objects.filter(block__is_active=True, block__flowchart_id=flowchart_id).order_by('-updated_date')
    #     return Comment.objects.filter(block__is_active=True).order_by('-updated_date')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if instance.author == user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message': "You are not author of this comment", 'error': True},
                        status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        flowchart_id = self.request.GET.get('flowchart_id')

        queryset = self.filter_queryset(self.get_queryset())
        if flowchart_id:
            queryset = queryset.filter(block__is_active=True, block__flowchart_id=flowchart_id)
        else:
            queryset = queryset.filter(block__is_active=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)






