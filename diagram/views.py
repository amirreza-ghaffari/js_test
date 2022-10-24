from django.shortcuts import render
from diagram.models import Block, Comment
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.


@login_required(login_url='users:login')
def block_info_view(request, pk):
    context = {}
    block = get_object_or_404(Block, id=pk)
    comments = Comment.objects.filter(block=block)
    context['comments'] = comments
    triggered_date = block.flowchart.triggered_date

    try:
        history_approve = block.history.filter(history_date__gte=
                                         triggered_date, is_approved=True).order_by('-history_date').values('history_date',
                                                                                          'history_user__email').last()
        context['approved'] = history_approve
    except:
        context['approved'] = None

    return render(request, 'diagram/block_info.html', context)














