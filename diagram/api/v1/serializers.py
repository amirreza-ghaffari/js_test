from rest_framework import serializers
from diagram.models import Block, Transition


class BlockSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source='id')
    text = serializers.CharField(source='label')

    class Meta:
        model = Block
        fields = ['key', 'text', 'figure', 'color', 'loc', 'thickness', 'fill']


class TransitionSerializer(serializers.ModelSerializer):
    from_ = serializers.CharField(source='start_block.id')
    to = serializers.CharField(source='end_block.id')

    class Meta:
        model = Transition
        fields = ['from_', 'to']

