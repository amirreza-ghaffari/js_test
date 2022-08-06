from django.db.models.signals import post_save
from .models import Transition, Block


def send_email(sender, instance, **kwargs):
    transition = instance
    block = transition.end_block
    print(f'email sent for the block {block} owners')


post_save.connect(send_email, sender=Transition)