import requests
import json
from .models import Block
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def custom_send_email(message, current_action, next_action, to_email_list, random_text, subject='BCM Management'):

    context = {'current_action': current_action, 'next_action': next_action, 'random_text': random_text}
    message = render_to_string('email/rac/rac.html', context=context)
    email = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, to_email_list)
    email.content_subtype = 'html'  # this is required because there is no plain text email version
    email.send(fail_silently=False)


def next_action(block, user):
    t = {}
    for b in Block.objects.filter(flowchart_id=block.flowchart_id).order_by('id'):
        out_block_ids, input_block_ids = [], []
        for transition in b.out_transition.all():
            out_block_ids.append(transition.end_block.id)

        for transition in b.input_transition.all():
            input_block_ids.append(transition.start_block.id)

        t[b.id] = {'next': out_block_ids, 'previous': input_block_ids}

    candidate_blocks = Block.objects.filter(user_groups__in=user.groups.all(), flowchart_id=block.flowchart_id).values_list('id', flat=True)
    next_blocks = t[block.id]['next']
    if 0 < len(next_blocks) < 2:
        if next_blocks[0] in candidate_blocks:
            return Block.objects.get(id=next_blocks[0])
    return None


def send_sms(phone_number, message):
    url = "https://sms.magfa.com/api/http/sms/v2/send"

    payload = json.dumps({
        "senders": [
            "98300061930014"
        ],
        "recipients": [
            phone_number
        ],
        "messages": [
            message
        ]
    })
    headers = {
        'Authorization': settings.SMS_PANEL_PASSWORD,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


















