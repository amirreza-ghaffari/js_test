import requests
import json
from diagram.models import Block
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from mattermostdriver.driver import Driver
from email.mime.image import MIMEImage
from functools import lru_cache
import string
import random

from js_test.business_rules import MATTERMOST_TEAM_NAME_TEST, MATTERMOST_GROUP_NAME_TEST, MATTERMOST_ACCOUNTS_TEST


def en2fa(string):
    if string.lower() == 'people_protest':
        return 'اعتراضات و اعتصابات مردمی'
    elif string.lower() == 'staff_strike':
        return 'شورش'
    elif string.lower() == 'seller_strike':
        return 'اعتصاب فروشندگان'

    elif string.lower() == 'earth_quake':
        return 'زمین لرزه'

    elif string.lower() == 'fire':
        return 'وقوع آتش سوزی'

    elif string.lower() == 'data_leakage':
        return 'درز اطلاعات'

    elif string.lower() == 'driver_strike':
        return 'اعتصاب رانندگان'

    return ''


def custom_send_email(context, to_email_list, flowchart_id=None, subject='Crisis Contingency Plan',
                      template_address='users/email.html'):
    rand_string = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=7)))
    context['rand_string'] = rand_string

    # set a flowchart_id in html to make it unique
    if flowchart_id:
        context['flowchart_id'] = flowchart_id
    template = render_to_string(template_address, context=context)
    email = EmailMultiAlternatives(subject, template, settings.EMAIL_HOST_USER, to_email_list)
    email.content_subtype = 'html'

    if flowchart_id:
        try:
            email.attach(screenshot_cache(flowchart_id, rand_string=rand_string))
        except Exception as e:
            print(e)

        try:
            email.attach(severity_cache(flowchart_id, rand_string=rand_string + '_severity'))
        except Exception as e:
            print(e)

    email.send(fail_silently=False)


def next_action(block, member):
    t = {}
    flowchart_id = block.flowchart_id
    for b in Block.objects.filter(flowchart_id=flowchart_id).order_by('id'):
        out_block_ids, input_block_ids = [], []
        for transition in b.out_transition.all():
            out_block_ids.append(transition.end_block.id)

        for transition in b.input_transition.all():
            input_block_ids.append(transition.start_block.id)

        t[b.id] = {'next': out_block_ids, 'previous': input_block_ids}

    candidate_blocks = Block.objects.filter(members=member, flowchart_id=flowchart_id,
                                            is_approved=False, is_active=False,
                                            is_pre_approved=False).values_list('id', flat=True)

    temp_id = block.id
    while True:
        next_blocks = t[temp_id]['next']
        if len(next_blocks) == 0:
            return None
        if next_blocks[0] in candidate_blocks:
            return Block.objects.get(id=next_blocks[0]).label
        temp_id = next_blocks[0]


def send_sms(phone_number_lst, message):
    url = "https://sms.magfa.com/api/http/sms/v2/send"

    payload = json.dumps({
        "senders": [
            "98300061930014"
        ],
        "recipients":
            phone_number_lst,
        "messages": [
            message
        ]
    })
    headers = {
        ''
        'Authorization': settings.SMS_PANEL_PASSWORD,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)['status']


def mattermost(usernames: list, msg: str):
    driver = Driver({
        'url': 'im.dkservices.ir',
        "token": settings.MM_TOKEN,
        'scheme': 'https',
        'port': 443
    })
    try:
        driver.login()

        res = driver.users.get_users_by_usernames(options=usernames)
        ids = []
        for item in res:
            ids.append(item['id'])

        if len(ids) < 2:
            return None
        res = driver.channels.create_direct_message_channel(options=ids)

        channel_id = res['id']

        res = driver.posts.create_post(options={
            'channel_id': channel_id,
            'message': msg
        })
    except Exception as e:
        print('Mattermost could not login: ', e)
        pass
    return None


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def loc_name(location):
    if location.lower() != 'no location':
        temp = ' در مطقه ی ' + location
        return temp
    return ''


@lru_cache()
def screenshot_cache(flowchart_id, rand_string):
    with open('media/screenshots/' + str(flowchart_id) + '/' + str(flowchart_id) + '.png', 'rb') as f:
        temp_data = f.read()
    img = MIMEImage(temp_data)
    img.add_header('Content-ID', '<' + rand_string + '>')
    return img


@lru_cache()
def severity_cache(flowchart_id, rand_string):
    with open('media/severity/' + str(flowchart_id) + '/' + str(flowchart_id) + '.png', 'rb') as f:
        temp_data = f.read()
    img = MIMEImage(temp_data)
    img.add_header('Content-ID', '<' + rand_string + '>')
    return img
