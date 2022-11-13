import json
import requests
from django.db.models import Q
from django.urls import reverse
from rest_framework.response import Response
from diagram.models import Block, Transition
from flowchart.models import Flowchart, Location, HistoryChange
from rest_framework import status


def f_create(flowchart_id, location_id):

    if flowchart_id == "0" or location_id == "0":
        return Response({'message': 'please select a location and a plan', 'error': True, 'error_code': 0},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        primary_flowchart = Flowchart.objects.get(id=flowchart_id, primary=True)
    except Flowchart.DoesNotExist:
        return Response({'message': 'Primary Flowchart Does not Exists', 'error': True, 'error_code': 1},
                        status=status.HTTP_404_NOT_FOUND)
    try:
        location_obj = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({'message': 'Location Does not Exists', 'error': True, 'error_code': 2},
                        status=status.HTTP_404_NOT_FOUND)

    flowchart, created = Flowchart.objects.get_or_create(name=primary_flowchart.name, location=location_obj)
    if not created:
        # f_end(flowchart.id)
        return Response({'message': 'Flowchart already exists', 'error_code': 3,
                         'flowchart_id': flowchart.id,
                         'url': reverse('flowchart:flowchart_view', kwargs={'pk': flowchart.id})},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    blocks = Block.objects.filter(flowchart=primary_flowchart).order_by('id')
    transitions = Transition.objects.filter((Q(start_block__in=blocks) | Q(end_block__in=blocks)))

    data = {}

    for block in blocks:
        block.pk = None
        block.is_approved = False
        block.is_active = False
        block.flowchart = flowchart
        block.save()
        data[block.label] = block.id

    for transition in transitions:
        transition.pk = None
        transition.is_active = False
        transition.is_approved = False
        start_block_name = transition.start_block.label
        end_block_name = transition.end_block.label
        transition.start_block_id = data[start_block_name]
        transition.end_block_id = data[end_block_name]
        transition.flowchart = flowchart
        transition.save()
    block = Block.objects.get(input_transition=None, flowchart_id=flowchart.id)
    block.is_active = True
    block.save()

    return Response({'message': 'new objects created', 'new_flowchart_id': flowchart.id, 'url': reverse('flowchart:flowchart_view', kwargs={'pk': flowchart.id})},
                    status=status.HTTP_201_CREATED)


def f_reset(flowchart_id):

    try:
        flowchart = Flowchart.objects.get(id=flowchart_id)
    except Flowchart.DoesNotExist:
        return Response({'message': 'flowchart does not exists', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)
    blocks = Block.objects.filter(flowchart__id=flowchart_id)
    transitions = Transition.objects.filter(start_block__in=blocks, end_block__in=blocks)
    for block in blocks:
        block.is_active = False
        block.is_approved = False
        block.is_pre_approved = False
        block.block_comment.all().delete()
        block.save()

    b = Block.objects.get(flowchart__id=flowchart_id, input_transition=None)
    b.is_active = True
    b.save()
    for tr in transitions:
        tr.is_approved = False
        tr.is_active = False
        tr.save()
    flowchart.is_active = False
    flowchart.save()
    return Response({'message': 'Flowchart reset successfully', 'error': False,
                     'url': reverse('flowchart:flowchart_view', kwargs={'pk': flowchart.id})},
                    status=status.HTTP_200_OK)


def f_end(flowchart_id):

    try:
        flowchart = Flowchart.objects.get(id=flowchart_id)
    except Flowchart.DoesNotExist:
        return Response({'message': 'flowchart does not exists', 'error': True},
                        status=status.HTTP_400_BAD_REQUEST)

    url = "http://127.0.0.1:8000/diagram/api/v1/block-history/" + str(flowchart_id) + "/"
    response = requests.request("GET", url)
    if response.status_code == 200:
        block_history = json.loads(response.text)
    else:
        block_history = {}

    url = "http://127.0.0.1:8000/diagram/api/v1/comment-history/" + str(flowchart_id) + "/"
    response = requests.request("GET", url)
    if response.status_code == 200:
        comment_history = json.loads(response.text)
    else:
        comment_history = {}

    try:
        if len(comment_history) > 0 or len(block_history) > 0:
            h = HistoryChange(flowchart=flowchart, comment_history=comment_history, block_history=block_history,
                              initial_date=flowchart.triggered_date)
            h.convert_to_j()
            h.save()

        flowchart.is_active = False
        flowchart.triggered_date = None
        flowchart.increase_incident()
        flowchart.save()

        f_reset(flowchart_id)

        return Response({"message": "ok"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)