from django.http import JsonResponse
from diagram.models import Block, Transition
from diagram.models import Flowchart
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required(login_url='users:login')
def flowchart_view(request, pk):
    context = {}

    try:
        flowchart = Flowchart.objects.get(pk=pk)
        context['flowchart_id'] = flowchart.id
        context['flowchart_name'] = flowchart.__str__().title()
        blocks = Block.objects.filter(Q(is_approved=True) | Q(is_active=True)).order_by('-updated_date')
        blocks = blocks.filter(flowchart_id=flowchart.id)
        context['blocks'] = blocks
    except Flowchart.DoesNotExist:
        return JsonResponse({'error': f'flowchart does not exists'})

    return render(request, 'flowchart/flowchart.html', context)


def new_flowchart(request, name):
    pass
