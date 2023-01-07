import imaplib
import requests
import json
from diagram.models import Block
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from mattermostdriver import Driver
from email.header import decode_header
import email
from bs4 import BeautifulSoup
from .models import Member, CustomUser, EmailResponse
from notifications.models import Notification
from notifications.signals import notify


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

def custom_send_email(context, to_email_list, subject='BCM Management', template_address='users/email.html'):

    template = render_to_string(template_address, context=context)
    email = EmailMultiAlternatives(subject, template, settings.EMAIL_HOST_USER, to_email_list)
    email.content_subtype = 'html'
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
    channel_id = res['id']

    res = driver.posts.create_post(options={
      'channel_id': channel_id,
      'message': msg
    })

    return None


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def email_response(n=5):
    imap = imaplib.IMAP4_SSL('mail.digikala.com')
    imap.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    # total number of emails
    messages = int(messages[0])
    if messages < n:
        n = messages

    for i in range(messages, messages - n, -1):
        # fetch the email message by ID
        body = None
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                from_, encoding = decode_header(msg.get("From"))[0]
                if isinstance(from_, bytes):
                    from_ = from_.decode(encoding)
                # print("Subject:", subject)
                # print("From:", from_)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                else:
                    body = msg.get_payload(decode=True).decode()
                if body:
                    soup = BeautifulSoup(body, "html.parser")
                    res_text = soup.find("body").text.split("From: Digikala Crisis.software")[0].strip().replace('\n\n', '')
                    member_email = from_.split('<')[1][:-1]
                    try:
                        member = Member.objects.get(email__iexact=member_email.lower())
                        email_res_obj, created = EmailResponse.objects.get_or_create(member=member, message=res_text)
                        if created:
                            notify.send(CustomUser.objects.first(), recipient=CustomUser.objects.all(), verb='you reached level 10', description=res_text)

                    except Member.DoesNotExist:
                        pass

    # close the connection and logout
    imap.close()
    imap.logout()


def loc_name(location):
    if location.lower() != 'no location':
        temp = ' در مطقه ی ' + location
        return temp
    return ''






