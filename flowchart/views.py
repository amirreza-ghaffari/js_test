from django.http import JsonResponse
from diagram.models import Block, Transition
from diagram.models import Flowchart
from django.shortcuts import render
from django.db.models import Q


def flowchart_view(request, name):
    context = {}

    try:
        flowchart = Flowchart.objects.get(name=name)
        context['flowchart_id'] = flowchart.id
        temp = flowchart.name
        context['flowchart_name'] = temp.replace('_', ' ').title()
        blocks = Block.objects.filter(Q(is_approved=True) | Q(is_active=True)).order_by('-updated_date')
        blocks = blocks.filter(flowchart_id=flowchart.id)
        context['blocks'] = blocks
    except Flowchart.DoesNotExist:
        return JsonResponse({'error': f'flowchart does not exists'})

    return render(request, 'flowchart/flowchart.html', context)


def new_flowchart(request, name):
    pass
