import requests
import json
from diagram.models import Block
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from mattermostdriver import Driver
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


def custom_send_email(context, to_email_list, flowchart_id=None, subject='BCM Management',
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
    driver.login()

    res = driver.users.get_users_by_usernames(options=usernames)
    ids = []
    for item in res:
        ids.append(item['id'])

    if len(ids) < 2:
        return None
    res = driver.channels.create_direct_message_channel(options=ids)

    # temp
    channel_x = driver.channels.get_channel_by_name_and_team_name(settings.MATTERMOST_TEAM_NAME,
                                                                  settings.MATTERMOST_CHANNEL_NAME)
    # create_private_channel()

    channel_id = res['id']

    res = driver.posts.create_post(options={
        'channel_id': channel_id,
        'message': msg
    })
    return None


def mattermost_post_in_channel_manager(
        msg, channel_name, team_name, file_path, msg_type='text', username_list=None, is_pinned=True, *args, **kwargs
):
    driver = mattermost_connection()
    mattermost_login(driver)
    channel_obj = mattermost_get_channel(driver, channel_name=channel_name, team_name=team_name)
    user_ids = mattermost_get_user_ids_from_usernames(driver=driver, username_list=username_list)

    if not channel_obj:
        team_id = mattermost_get_team_by_name(driver, team_name)
        channel_obj = mattermost_create_channel(driver, team_id, channel_name)
    are_added, failed_to_create_users = mattermost_add_users_to_channel(driver, channel_obj.get("id"), user_ids)
    if isinstance(channel_obj, dict):
        mattermost_post_in_channel(
            driver=driver, channel_id=channel_obj.get("id"), msg=msg,
            msg_type=msg_type, file_path=file_path, is_pinned=is_pinned
        )
    return True


def mattermost_connection(url=None, token=None, *args, **kwargs):
    driver = Driver({
        'url': 'im.dkservices.ir',
        "token": settings.MM_TOKEN,
        'scheme': 'https',
        'port': 443
    })
    return driver if driver else False


def mattermost_login(driver):
    try:
        result = driver.login()
        return result if result else False
    except Exception as e:
        return False


def mattermost_get_team_by_name(driver, team_name):
    try:
        return driver.teams.get_team_by_name(team_name).get('id')
    except Exception as e:
        return False


def mattermost_get_channel(driver, channel_name, team_name):
    try:
        channel = driver.channels.get_channel_by_name_and_team_name(team_name, channel_name)
        return channel
    except Exception as e:
        return False


def mattermost_get_user_ids_from_usernames(driver, username_list):
    try:
        user_ids = []
        users_obj_list = driver.users.get_users_by_usernames(options=username_list)
        [user_ids.append(user.get('id')) for user in users_obj_list if user]
        return user_ids
    except Exception as e:
        return False


def mattermost_create_channel(driver, team_id, channel_name):
    try:
        return driver.channels.create_channel(options={
            "team_id": team_id,
            "name": channel_name,
            "display_name": channel_name,
            "purpose": "Business Continuity Management Group",
            "header": "Business Continuity Management",
            "type": "P"  # Private Channel
        })
    except Exception as e:
        return False


def mattermost_add_users_to_channel(driver, channel_id, user_ids):
    try:
        failed_usernames = []
        for user_id in user_ids:
            try:
                driver.channels.add_user(channel_id, options={'user_id': user_id})
            except Exception as e:
                failed_usernames.append(driver.users.get_user(user_id).get('username'))

        return True, failed_usernames
    except Exception as e:
        return {}


def mattermost_post_in_channel(driver, channel_id, msg, file_path, is_pinned, msg_type='text'):
    post = {}
    try:
        if channel_id:
            if msg_type == 'text':
                post = driver.posts.create_post(options={
                    'channel_id': channel_id,
                    'message': msg
                })
                if is_pinned:
                    driver.posts.pin_post_to_channel(post_id=post.get('id'))

            elif msg_type == 'file':
                form_data = {
                    "channel_id": ('', channel_id),
                    "client_ids": ('', "id_for_the_file"),
                    "files": (file_path, open(file_path, 'rb')),
                }
                file_post = driver.files.upload_file(channel_id, form_data)
                file_id = file_post.get("file_infos")[0].get("id")
                driver.posts.create_post(options={
                    'channel_id': channel_id,
                    'message': 'Hi...',
                    "file_ids": [file_id]
                })

            return True if post else False
    except Exception as e:
        return False


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





# Temp
mattermost_post_in_channel_manager(
    msg='post has been pinned successfully!', channel_name=MATTERMOST_GROUP_NAME_TEST,
    team_name=MATTERMOST_TEAM_NAME_TEST,
    msg_type='text', file_path='/home/omid/Music/In-The-End.mp3',
    username_list=MATTERMOST_ACCOUNTS_TEST
)