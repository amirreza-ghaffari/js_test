from rest_framework import serializers
from flowchart.models import Flowchart, Location
from django.contrib.auth import get_user_model
User = get_user_model()


class FlowchartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flowchart
        fields = ['id', 'get_absolute_url', '__str__']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = representation['__str__']
        representation.pop('__str__')
        return representation


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'incident_number']

