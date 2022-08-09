from django.db.models.signals import post_save
from .models import Transition, Block
from django.conf import settings
from django.core.mail import send_mail


def notif_staff_signal(sender, instance, **kwargs):

    block = instance.end_block
    message = f' Block with state name {block.label}  need to be approved'
    send_mail('BCM Management', message, settings.EMAIL_HOST_USER, ['h.pourhaji@digikala.com'])
    print(f'email sent for the block {block} owners')


post_save.connect(notif_staff_signal, sender=Transition)