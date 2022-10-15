import json
from django.http import JsonResponse
from diagram.models import Block, Transition
from .models import Flowchart, HistoryChange
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import jdatetime


@login_required(login_url='users:login')
def flowchart_view(request, pk):
    context = {}

    try:
        flowchart = Flowchart.objects.get(pk=pk)
        t = flowchart.triggered_date
        if t:
            j = jdatetime.datetime.fromgregorian(day=t.day, month=t.month, year=t.year, hour=t.hour, minute=t.minute)
            context['triggered_date'] = j
        context['flowchart_id'] = flowchart.id
        context['flowchart_name'] = flowchart.__str__().title()
        blocks = Block.objects.filter(Q(is_approved=True) | Q(is_active=True)).order_by('-updated_date')
        blocks = blocks.filter(flowchart_id=flowchart.id)
        context['blocks'] = blocks
    except Flowchart.DoesNotExist:
        return JsonResponse({'error': f'flowchart does not exists'})

    if flowchart.primary:
        return render(request, 'flowchart/primary_flowchart.html', context)

    return render(request, 'flowchart/flowchart.html', context)


@login_required(login_url='users:login')
def history_detail(request, pk):
    context = {}
    history = get_object_or_404(HistoryChange, pk=pk)
    block_h = json.loads(history.block_history)
    comment_h = json.loads(history.comment_history)
    flowchart = Flowchart.objects.get(id=history.flowchart.id)

    context['block_history'] = block_h
    context['comment_history'] = comment_h
    context['flowchart'] = flowchart
    context['history_id'] = history.id

    return render(request, 'flowchart/history_detail.html', context)


@login_required(login_url='users:login')
def history_list(request):
    context = {}
    histories = HistoryChange.objects.filter(flowchart__primary=False).order_by('-initial_date')
    for history in histories:
        m = history.initial_date
        jalali = jdatetime.datetime.fromgregorian(day=m.day, month=m.month, year=m.year, hour=m.hour, minute=m.minute)
        history.jalali = jalali
    context['histories'] = histories

    return render(request, 'flowchart/history_list.html', context)
