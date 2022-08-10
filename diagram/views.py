from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Block, Transition
from django.contrib import messages


# Create your views here.


@login_required
def approved_block(request, block_label):
    user = request.user

    try:
        start_block = Block.objects.get(label=block_label)
    except Block.DoesNotExist:
        return JsonResponse({'error': f'This block with label "{block_label}" does not exists'})

    if start_block.user_groups and user not in start_block.user_groups.user_set.all():
        return JsonResponse({'error': f'The user {user} does not have permission for block "{block_label}"!'})

    if start_block.active:
        start_block_group = start_block.group
        start_block.approved = True
        start_block.active = False
        start_block.color = 'green'
        start_block.save()

        group_approved_flag = True

        for block_obj in Block.objects.filter(group=start_block_group).all():
            if block_obj.approved is False and block_obj.group:
                group_approved_flag = False

        try:
            transients = Transition.objects.filter(start_block=start_block)
            for transient_obj in transients:
                end_block = transient_obj.end_block

                if (end_block.group and end_block.group == start_block_group) or (start_block_group is None) or (group_approved_flag):
                    transient_obj.active = True
                    transient_obj.save()
                    #  send email or sms or print in terminal #
                    end_block.active = True
                    end_block.color = 'red'
                    end_block.save()

        except Transition.DoesNotExist:
            return JsonResponse(
                {'error': f'This block {start_block} does not has transient'})
        return JsonResponse({'detail': f'Block with id {start_block.id} and label {start_block.label} approved successfully'})
    else:
        return JsonResponse({'error': f'This block with id {start_block.id} and label {start_block.label} has not been activated yet'})















