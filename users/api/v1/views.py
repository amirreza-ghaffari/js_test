from flowchart.models import Flowchart
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from ...models import Member
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import permissions
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from diagram.utils import send_sms
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import ast


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def sens_sms_view(request):
    members_id = request.data.get('members')
    members_id = ast.literal_eval(members_id)
    print(members_id)
    members_id = [int(x) for x in members_id]

    message = request.data.get('message')
    members_mobile_lst = list(Member.objects.filter(id__in=members_id).values_list('mobile_number', flat=True))
    x = send_sms(phone_number_lst=members_mobile_lst, message=message)
    return Response({'message': 'send'}, status=status.HTTP_200_OK)









