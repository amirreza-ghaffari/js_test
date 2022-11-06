from django.db.models.signals import post_save
from .models import Transition, Block
from django.utils.crypto import get_random_string
import datetime
from flowchart.utils import f_end


def active_transition_on_block_approve(sender, instance, created, **kwargs):
    try:
        start_block = instance
        flowchart = start_block.flowchart
        if start_block.is_approved:
            end_blocks = flowchart.blocks.filter(out_transition=None)

            if len(start_block.input_transition.all()) == 0:
                flowchart.is_active = True
                flowchart.triggered_date = datetime.datetime.now()
                flowchart.save()

            if end_blocks.count() > 0:
                if end_blocks.count() == end_blocks.filter(is_approved=True).count():
                    f_end(flowchart.id)

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
    except Exception as e:
            print(e)


post_save.connect(active_transition_on_block_approve, sender=Block)


def active_block_on_transient_approve(sender, instance, **kwargs):
    try:
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
    except Exception as e:
        print(e)


post_save.connect(active_block_on_transient_approve, sender=Transition)