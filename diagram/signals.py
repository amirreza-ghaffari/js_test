from django.db.models.signals import post_save
from .models import Transition, Block
from .utils import custom_send_email


def notif_staff_signal(sender, instance, **kwargs):

    block = instance.end_block
    message = f' Block with state name {block.label}  need to be approved'
    # custom_send_email(message, ['xx@gmail.com'])
    print(f'email sent for the block {block} owners')


post_save.connect(notif_staff_signal, sender=Transition)