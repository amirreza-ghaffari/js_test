from rest_framework import serializers
from flowchart.models import Flowchart
from django.contrib.auth import get_user_model
User = get_user_model()


class FlowchartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flowchart
        fields = ['name', 'get_absolute_url']



