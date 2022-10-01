from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from ...models import Member
from rest_framework import status
from rest_framework.response import Response
from diagram.utils import send_sms, custom_send_email
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import ast


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def send_sms_api(request):
    members_id = request.data.get('members')
    members_id = ast.literal_eval(members_id)
    members_id = [int(x) for x in members_id]

    message = request.data.get('message')
    members_mobile_lst = list(Member.objects.filter(id__in=members_id).values_list('mobile_number', flat=True))
    try:
        x = send_sms(phone_number_lst=members_mobile_lst, message=message)
        return Response({'message': 'message sent'}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'could not send message'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def send_email_api(request):
    try:
        members_id = request.data.get('members')
        members_id = ast.literal_eval(members_id)
        members_id = [int(x) for x in members_id]

        message = request.data.get('message')
        members_email_lst = list(Member.objects.filter(id__in=members_id).values_list('email', flat=True))
        custom_send_email({'message': message}, members_email_lst, template_address='email/mail2.html')
        return Response({'message': 'message sent'}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'could not send message'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
