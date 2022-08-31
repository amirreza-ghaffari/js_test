from django.db.models.signals import post_save
from .models import Transition, Block
from .utils import custom_send_email, find_next_action
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings



def active_transition_on_block_approve(sender, instance, **kwargs):
    start_block = instance
    if start_block.is_approved:

        transients = Transition.objects.filter(start_block=start_block)
        for obj in transients:
            if not start_block.is_conditional:
                obj.is_approved = True
            else:
                obj.is_active = True
            obj.save()

post_save.connect(active_transition_on_block_approve, sender=Block)


def active_block_on_transient_approve(sender, instance, **kwargs):
    transient = instance
    if transient.is_approved:
        end_block = transient.end_block
        start_block = transient.start_block
        if start_block.is_conditional:
            transients = Transition.objects.filter(start_block=start_block).exclude(id=transient.id)
            for tr in transients:
                tr.is_active = False
                tr.save()

        end_block.is_active = True
        end_block.save()

        if not end_block.is_conditional:
            for group in end_block.user_groups.all():
                next_action = find_next_action(end_block, group)
                print('send to block  ' + end_block.label + 'owners:', group)
                print(end_block.label , next_action)
                custom_send_email('salam', end_block.label, next_action, ['amirreza.ghaffari.d@gmail.com'])

post_save.connect(active_block_on_transient_approve, sender=Transition)