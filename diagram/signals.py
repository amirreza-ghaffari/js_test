from django.db.models.signals import post_save
from .models import Transition, Block
from .utils import custom_send_email


def notif_staff_signal(sender, instance, **kwargs):

    block = instance.end_block
    message = f' Block with state name {block.label}  need to be approved'
    # custom_send_email(message, ['xx@gmail.com'])
    print(f'email sent for the block {block} owners')


post_save.connect(notif_staff_signal, sender=Transition)


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
        end_block.is_active = True
        end_block.save()


post_save.connect(active_block_on_transient_approve, sender=Transition)