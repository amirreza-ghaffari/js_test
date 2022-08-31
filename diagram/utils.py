from django.conf import settings
from django.core.mail import send_mail
from .models import Block, Transition
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


html_version = 'email/rac/rac.html'


def custom_send_email(message, current_action, next_action, to_email_list, subject='BCM Management'):

    context = {'current_action': current_action, 'next_action': next_action}
    message = render_to_string(html_version, context=context)
    email = EmailMultiAlternatives(subject, message , settings.EMAIL_HOST_USER, to_email_list)
    email.content_subtype = 'html'  # this is required because there is no plain text email version
    email.send(fail_silently=False)



def next_block(transient):
    return transient.end_block

def next_transitions(block):
    return Transition.objects.filter(start_block=block)



def find_next_action(block, group):
    nex_action = None
    try:
        block = Block.objects.filter(user_groups=group, is_active=False, is_approved=False).first()
        nex_action = block.label
    except Block.DoesNotExist:
        pass

    return nex_action



















