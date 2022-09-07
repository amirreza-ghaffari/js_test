from django.conf import settings
from .models import Block
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


html_version = 'email/rac/rac.html'


def custom_send_email(message, current_action, next_action, to_email_list, random_text, subject='BCM Management'):

    context = {'current_action': current_action, 'next_action': next_action, 'random_text': random_text}
    message = render_to_string(html_version, context=context)
    email = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, to_email_list)
    email.content_subtype = 'html'  # this is required because there is no plain text email version
    email.send(fail_silently=False)


def find_next_action(block, group):
    nex_action = None
    try:
        block = Block.objects.filter(user_groups=group, is_active=False, is_approved=False).first()
        nex_action = block.label
    except Block.DoesNotExist:
        pass

    return nex_action



















