from django.db.models.signals import post_save
from .models import Transition, Block
from .utils import custom_send_email, next_action
from django.utils.crypto import get_random_string
from users.models import CustomUser


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
            for user_id in end_block.user_groups.all().values_list('user__id', flat=True).distinct():
                if user_id:
                    user = CustomUser.objects.get(id=user_id)
                    next_action_block = next_action(end_block, user)
                    random_text = user.rand_text + '_' + str(end_block.id)
                    print('user:', user, 'block:', end_block, 'next_action: ', next_action_block)
                    context = {'current_action': end_block.label, 'next_action': next_action, 'random_text': random_text}
                    # custom_send_email(context, ['h.pourhaji@digikala.com'])


post_save.connect(active_block_on_transient_approve, sender=Transition)