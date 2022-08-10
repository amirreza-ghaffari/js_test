from rest_framework import serializers
from diagram.models import Block, Transition
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model
User = get_user_model()

class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields = ['figure', 'color', 'loc', 'thickness', 'fill']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['key'] = instance.id
        representation['text'] = instance.label
        return representation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'department', 'full_name']

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


class HistorySerializer(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()
    class Meta:
        model = Block
        fields = ('id', 'history',)
        read_only_fields = ('history',)

    def get_history(self, obj):
        # using slicing to exclude current field values
        h = obj.history.all().values('history_user', 'label')
        return h


class CustomerHistorySerializer(serializers.ModelSerializer):
    history_user = UserSerializer(many=False)
    class Meta:
        model = Block.history.model
        fields = ['history_id', 'history_date', 'history_user', 'label', 'active', 'approved']