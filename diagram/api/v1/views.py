import jdatetime
from flowchart.models import Flowchart
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.contrib.humanize.templatetags.humanize import naturaltime
from ...models import Block, Transition, Comment
from .serializers import BlockSerializer, TransitionSerializer, Custom2, CommentSerializer
from rest_framework import status, permissions
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

    serializer_class = BlockSerializer
    queryset = Block.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['flowchart', 'is_approved', 'is_active', 'is_pre_approved']


class TransitionViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_approved', 'is_active']

    permission_classes = [IsAuthenticated]
    serializer_class = TransitionSerializer

    def get_queryset(self):
        flowchart_id = self.request.query_params.get('flowchart_id')
        if flowchart_id:
            blocks = Block.objects.filter(flowchart_id=flowchart_id)
            return Transition.objects.filter(start_block__in=blocks, end_block__in=blocks)
        return Transition.objects.all()


class BlockHistory(ViewSet):

    # permission_classes = [IsAuthenticated]
    serializer_class = Custom2
    queryset = Flowchart.objects.all()

    def retrieve(self, request, pk=None):
        t = {}
        flowchart = get_object_or_404(self.queryset, pk=pk)
        blocks = Block.objects.filter(flowchart=flowchart, flowchart__is_active=True).order_by('-updated_date', '-id')
        for block in blocks:
            histories = block.history.all()
            if len(histories) > 1:
                new_record, old_record = block.history.all()[0:2]
                delta = new_record.diff_against(old_record, included_fields=['is_approved'])
                if len(delta.changes) > 0:
                    serializer = self.serializer_class(delta.changes, many=True)
                    data = serializer.data
                    try:
                        user = new_record.history_user.full_name
                        change_date = new_record.history_date
                        z = {'label': block.label, 'changes': data, 'user': user,
                             'change_date':
                                 str(jdatetime.datetime.fromgregorian(day=change_date.day, month=change_date.month,
                                                                      year=change_date.year, hour=change_date.hour,
                                                                      minute=change_date.minute))}
                        t[block.id] = z
                    except:
                        pass
        if len(t) > 0:
            return Response(t, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'this object has no history_change change or is not active yet'},
                            status=status.HTTP_404_NOT_FOUND)


class CommentHistory(ViewSet):

    # permission_classes = [IsAuthenticated]
    serializer_class = Custom2
    queryset = Flowchart.objects.all()

    def retrieve(self, request, pk=None):
        t = {}
        flowchart = get_object_or_404(self.queryset, pk=pk)
        blocks = Block.objects.filter(flowchart=flowchart, flowchart__is_active=True)
        comments = Comment.objects.filter(block__in=blocks).order_by('id')
        for comment in comments:
            updated_date = comment.updated_date
            z = {'block': comment.block.label,'block_id': comment.block.id, 'label': comment.label, 'text': comment.text, 'author': comment.author.full_name, 'date': str(jdatetime.datetime.fromgregorian(
                        day=updated_date.day, month=updated_date.month, year=updated_date.year, hour=updated_date.hour,
                        minute=updated_date.minute))}
            if len(comment.history.all()) > 1:
                new_record, old_record = comment.history.all()[0:2]
                delta = new_record.diff_against(old_record, included_fields=['text'])
                if len(delta.changes) > 0:
                    serializer = self.serializer_class(delta.changes, many=True)
                    data = serializer.data
                    user = new_record.history_user.full_name
                    change_date = new_record.history_date
                    z['changes'] = {'changes': data, 'user': user, 'change_date': str(jdatetime.datetime.fromgregorian(
                        day=change_date.day, month=change_date.month, year=change_date.year, hour=change_date.hour,
                        minute=change_date.minute))}
            t[comment.id] = z
        if len(t) > 0:
            return Response(t, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'this object has no history_change change or is not active yet'},
                            status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        flowchart_id = self.request.query_params.get('flowchart_id')
        if flowchart_id:
            blocks = Block.objects.filter(flowchart_id=flowchart_id, is_active=True)
            return Comment.objects.filter(block__in=blocks).order_by('-updated_date')
        return Comment.objects.all()

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        if instance.author == user or instance.author.is_superuser:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message': "You are not authorize to delete this comment", 'error': True},
                        status=status.HTTP_401_UNAUTHORIZED)





