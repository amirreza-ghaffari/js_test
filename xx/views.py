import json
from diagram.models import Block
from django.shortcuts import render


# Create your views here.


def index(request):
    context = {}

    user = request.user

    groups = user.groups.all()

    block_list = []
    for group in groups:
        print(group)
        blocks = Block.objects.filter(user_groups=group)
        for block in blocks:
            block_list.append(block)
        context['block'] = block_list
    print(context)
    return render(request, 'blockEditor.html', context)

