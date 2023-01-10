from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from ...models import Member
from diagram.models import Block
from rest_framework import status
from rest_framework.response import Response
from users.utils import send_sms, custom_send_email, next_action, mattermost, en2fa, loc_name
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
def custom_send_smg(request):
    try:
        members_id = request.data.get('members')
        members_id = ast.literal_eval(members_id)
        members_id = [int(x) for x in members_id]
        members = Member.objects.filter(id__in=members_id)

        msg_type = request.data.get('msg_type')
        msg_type = ast.literal_eval(msg_type)
        msg_type = [str(x) for x in msg_type]

    except:
        return Response({'message': 'no member or msg_type provided'}, status=status.HTTP_400_BAD_REQUEST)

    msg_text = request.data.get('text')
    if len(members_id) > 0 and msg_text != '':
        if 'sms' in msg_type:
            mobile_lst = list(members.values_list('mobile_number', flat=True))
            status_code = send_sms(mobile_lst, msg_text)

        if 'mm' in msg_type:
            for member in members:
                username = member.email.replace('@digikala.com', '')
                mattermost(['amirreza.ghafari', username], msg_text)

        if 'email' in msg_type:
            email_lst = list(members.values_list('email', flat=True))
            context = {'current_action': msg_text}
            custom_send_email(context, email_lst, subject='BCM Management', template_address='users/email.html')

    return Response({'message': 'message sent'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def send_block_msg(request):
    try:
        members_id = request.data.get('members')
        members_id = ast.literal_eval(members_id)
        members_id = [int(x) for x in members_id]
        members = Member.objects.filter(id__in=members_id)

        msg_type = request.data.get('msg_type')
        msg_type = ast.literal_eval(msg_type)
        msg_type = [str(x) for x in msg_type]

        msg_text = request.data.get('text')
        block_id = request.data.get('block_id')

    except Exception as e:
        return Response({'message': 'There is a error in input data', 'detail': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)

    if msg_text == '':
        return Response({'message': 'No message inserted'},
                        status=status.HTTP_400_BAD_REQUEST)

    if len(members) > 0 and len(msg_type) > 0 and block_id and msg_text != '':

        block = Block.objects.get(id=block_id)
        if len(block.input_transition.all()) == 0 or block.label == 'شروع':
            msg_text = "بحرانی با موضوع " + en2fa(block.flowchart.name) + loc_name(
                block.flowchart.location.name) + " اتفاق افتاد"
        flowchart_name = block.flowchart.name
        block.members.add(*members)
        block.save()

        for member in members:
            if 'sms' in msg_type:
                mobile_lst = [member.mobile_number]
                sms_text = 'جناب آقای / خانم ' + member.full_name + "\n" * 2 + "با توجه به وقوع بحران " + en2fa(block.flowchart.name) + loc_name(block.flowchart.location.name) + "، لیست اقادامات شما به شرح زیر است: " + "\n" * 2 + msg_text
                status_code = send_sms(mobile_lst, sms_text)

            if 'email' in msg_type:
                context = {'current_action': msg_text, 'name': member.full_name,
                           'contingency_name': flowchart_name.replace('_', ' ').title(),
                           'flowchart_name': en2fa(flowchart_name),
                           'next_action': next_action(block, member) if block else None}
                custom_send_email(context, [member.email], subject='BCM Management',
                                  template_address='users/email.html')

            if 'mm' in msg_type:
                username = member.email.replace('@digikala.com', '')
                mattermost(['digikalacrisis.softw', username], sms_text)

    return Response({'message': 'message sent'}, status=status.HTTP_200_OK)
