from rest_framework import serializers
from flowchart.models import Flowchart, Location
from django.contrib.auth import get_user_model
User = get_user_model()


class FlowchartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flowchart
        fields = ['id', 'name', 'get_absolute_url']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'incident_number']

