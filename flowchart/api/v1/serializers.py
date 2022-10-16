from rest_framework import serializers
from flowchart.models import Flowchart, Location, HistoryChange
from django.contrib.auth import get_user_model
User = get_user_model()


class FlowchartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flowchart
        fields = ['id', 'get_absolute_url', '__str__', 'p_triggered_date']
        read_only_fields = ['p_triggered_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = representation['__str__']
        representation.pop('__str__')
        return representation


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'incident_number']


class HistoryChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryChange
        fields = ['id', 'comment_history', 'block_history']