from django.conf import settings
from django.core.mail import send_mail
from .models import Block, Transition


def custom_send_email(message, to_email_list, subject='BCM Management'):
    send_mail(subject, message, settings.EMAIL_HOST_USER, to_email_list)



def next_block(transient):
    return transient.end_block

def next_transitions(block):
    return Transition.objects.filter(start_block=block)



def find_next_contingency(transient):
    end_block = transient.end_block
    groups = end_block.user_groups.all()
    group = groups[0]


    blocks = Block.objects.filter(user_groups=group)


















