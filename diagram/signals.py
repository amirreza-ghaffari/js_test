from django.db.models.signals import post_save
from .models import Transition, Block
from .utils import custom_send_email, find_next_action
from django.utils.crypto import get_random_string


def active_transition_on_block_approve(sender, instance, created, **kwargs):
    start_block = instance
    if start_block.is_approved:

        transients = Transition.objects.filter(start_block=start_block)
        for obj in transients:
            if not start_block.is_conditional:
                obj.is_approved = True
            else:
                obj.is_active = True
            obj.save()
        return None
    if created:
        instance.rand_text = get_random_string(length=16)
        instance.save()


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
                # next_action = find_next_action(end_block, group)
                next_action = None
                for user in group.user_set.all():
                    random_text = user.rand_text + '_' + str(end_block.id)
                    print('user:', user, 'block:', end_block.label)
                    # custom_send_email('salam', end_block.label, next_action, ['amirreza.ghaffari.d@gmail.com'],
                    #                   random_text)


post_save.connect(active_block_on_transient_approve, sender=Transition)