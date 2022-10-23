from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from ...models import Member
from diagram.models import Block
from rest_framework import status
from rest_framework.response import Response
from users.utils import send_sms, custom_send_email
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from diagram.api.v1.serializers import MemberSerializer
import ast


class MemberViewSet(ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def send_msg(request):

    try:
        members_id = request.data.get('members')
        members_id = ast.literal_eval(members_id)
        members_id = [int(x) for x in members_id]

        msg_type = request.data.get('msg_type')
        msg_type = ast.literal_eval(msg_type)
        msg_type = [str(x) for x in msg_type]

    except:
        return Response({'message': 'no member or msg_type provided'}, status=status.HTTP_400_BAD_REQUEST)

    block_id = request.data.get('block_id')
    msg_text = request.data.get('text')
    if block_id:
        block = Block.objects.get(id=block_id)
        if msg_text:
            text = msg_text
        else:
            text = block.label
    else:
        text = msg_text

    print(text)
    try:
        if len(members_id) > 0 and text != '' and text:
            queryset = Member.objects.filter(id__in=members_id)
            if 'sms' in msg_type:
                mobile_lst = list(queryset.values_list('mobile_number', flat=True))
                status_code = send_sms(mobile_lst, text)

            if 'email' in msg_type:
                email_lst = list(queryset.values_list('email', flat=True))
                context = {'current_action': text, 'next_action': None}
                custom_send_email(context, email_lst, subject='BCM Management', template_address='email/rac/rac.html')

        return Response({'message': 'message sent'}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'There is a Error'}, status=status.HTTP_400_BAD_REQUEST)