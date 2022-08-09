from rest_framework import serializers
from diagram.models import Block, Transition



class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields = ['figure', 'color', 'loc', 'thickness', 'fill']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['key'] = instance.id
        representation['text'] = instance.label
        return representation


class TransitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transition
        fields = ['start_block', 'end_block']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['from'] = instance.start_block.id
        representation['to'] = instance.end_block.id
        #TODO: add time for transitions

        # if instance.active:
        #     representation['text'] = 'Activated in ' + instance.last_modified
        representation.pop('start_block')
        representation.pop('end_block')
        return representation

