import json

from django.shortcuts import render
import requests

# Create your views here.

context = {}


def index(request):

    a = {"class": "GraphLinksModel"}


    url_transition = 'http://127.0.0.1:8000/diagram/api/v1/transitions/'
    url_block = 'http://127.0.0.1:8000/diagram/api/v1/blocks/'

    api_call = requests.get(url_transition, headers={})
    transition = api_call.json()

    for x in transition:
        x['from'] = x['from_']
        x.pop('from_')

    api_call = requests.get(url_block, headers={})
    block = api_call.json()

    a["nodeDataArray"] = block

    a[ "linkDataArray"] = transition

    a = json.dumps(a)
    print(a)

    return render(request, 'blockEditor.html', {'a': a})
