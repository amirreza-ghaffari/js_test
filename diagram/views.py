from django.shortcuts import render
from django.http import JsonResponse

from .models import Block, Transition

# Create your views here.


def approved_block(request, block_label):
    user = request.user

    start_block = Block.objects.get(label=block_label)

    if start_block.active:

        start_block.approved = True
        start_block.active = False
        start_block.color = 'green'
        start_block.save()

        print(f'Block with id {start_block.id} and label {start_block.label} approved successfully')

        try:
            transients = Transition.objects.filter(start_block=start_block)
            for obj in transients:
                obj.active = True
                obj.save()

                'send email or sms or print in terminal'

                end_block = obj.end_block
                end_block.active = True
                end_block.save()

        except Transition.DoesNotExist:
            pass




        return JsonResponse({'detail': f'Block with id {start_block.id} and label {start_block.label} approved successfully'})
    else:
        return JsonResponse({'error': f'This block with id {start_block.id} and label {start_block.label} has not been activated yet'})















