import time
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from js_test.business_rules import CONTINGENCY_NAMES_VIEW, CALLER_SERVER_ADDRESS
from tools.general import manager_caller_to_list_numbers
from ...models import Member
from diagram.models import Block
from rest_framework import status
from flowchart.models import Flowchart
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

        msg_text = request.data.get('text')
        if not msg_text:
            raise ValueError('message is Empty')
    except Exception as e:
        print(e)
        return Response({'message': 'no member or msg_type provided'}, status=status.HTTP_400_BAD_REQUEST)

    msg_text = request.data.get('text')

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
    start_flag = False
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

    try:
        block = Block.objects.get(id=block_id)
        flowchart_name = block.flowchart.name
        block.members.add(*members)
        block.save()
    except:
        return Response({'message': 'block_id is not valid'},
                        status=status.HTTP_400_BAD_REQUEST)

    if len(block.input_transition.all()) == 0:
        start_flag = True

    for member in members:

        if 'email' in msg_type:
            context = {'current_action': msg_text if start_flag is False else 'آماده باش برای بحران و پیگیری اطلاع رسانی ها و دستورالعمل های آتی',
                       'name': member.full_name,
                       'contingency_name': flowchart_name.replace('_', ' ').title(),
                       'flowchart_name': en2fa(flowchart_name),
                       'next_action': None}
            # ---- for creating Delay between send MSG and save screenshot  API ---- #
            time.sleep(3)
            custom_send_email(context, [member.email], flowchart_id=block.flowchart.id, subject='BCM Management',
                              template_address='users/email.html')

        if start_flag:
            text = "بحرانی با موضوع " + en2fa(block.flowchart.name) + loc_name(
                block.flowchart.location.name) + " شروع شده است" + "\n" + " لطفا به طور پیوسته ایمیل و پیامک و Mattermost خود را چک کنید."
        else:
            text = 'جناب آقای / خانم ' + member.full_name + "\n" * 2 + "با توجه به وقوع بحران " + en2fa(
                block.flowchart.name) + loc_name(
                block.flowchart.location.name) + "، لیست اقدامات شما به شرح زیر است: " + "\n" + msg_text

        if 'mm' in msg_type:
            username = member.email.replace('@digikala.com', '')
            mattermost(['digikalacrisis.softw', username], text)

        if 'sms' in msg_type:
            mobile_lst = [member.mobile_number]
            status_code = send_sms(mobile_lst, text)

        # Call to numbers just at first step
    if start_flag:
        manager_caller_to_list_numbers(
            url=CALLER_SERVER_ADDRESS,
            number_list=members.values_list('mobile_number', flat=True),
            call_type=CONTINGENCY_NAMES_VIEW.get(block.flowchart.name)
        )

    return Response({'message': 'message sent'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def call_members(request):
    try:
        flowchart_id = request.data.get('flowchart_id')
        flowchart = Flowchart.objects.get(id=flowchart_id)
        queryset = flowchart.blocks.all()
        start_block = queryset.filter(input_transition=None)[0]
        members = start_block.members.all()

        manager_caller_to_list_numbers(
            url=CALLER_SERVER_ADDRESS,
            number_list=members.values_list('mobile_number', flat=True),
            call_type=CONTINGENCY_NAMES_VIEW.get(flowchart.name)
        )
    except:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Caller ringed successfully'}, status=status.HTTP_200_OK)


