from rest_framework import serializers
from diagram.models import Block, Transition, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from users.models import Member

User = get_user_model()


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id',)


class BlockSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    loc = serializers.CharField(max_length=256)

    class Meta:
        model = Block
        fields = ['label', 'figure', 'color', 'is_approved', 'is_pre_approved', 'loc_height', 'loc_length',
                  'flowchart', 'loc', 'members']

    def validate(self, data):
        loc = data.pop('loc', None)
        orig_instance = self.instance
        new_instance = Block(**data)
        if new_instance.is_approved and (orig_instance.is_active is False or orig_instance.is_pre_approved is False):
            raise serializers.ValidationError('Can not approve a non active or none pre_approved Block')

        if new_instance.is_pre_approved and orig_instance.is_active is False:
            raise serializers.ValidationError('Can not Pre_approve a non active block')

        if new_instance.is_approved:
            orig_instance.is_active = False
            data['is_active'] = False

        if loc:
            data['loc_height'], data['loc_length'] = loc.split(' ')

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['key'] = instance.id
        representation['text'] = instance.label
        representation.pop('is_approved')
        representation.pop('loc_length')
        representation.pop('loc_height')
        representation.pop('label')
        if instance.is_conditional:
            representation['size'] = "600 350"
        else:
            representation['size'] = "450 150"

        if instance.is_active and not instance.is_conditional:
            representation['figure'] = "CreateRequest"
        if len(instance.out_transition.all()) == 0:
            representation['figure'] = "Ellipse"

        representation['fill'] = "beige"
        representation['thickness'] = 4
        representation.pop('flowchart')
        representation['block_info'] = instance.block_info
        return representation


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'department', 'full_name']


class TransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = ['start_block', 'end_block', 'is_approved', 'color', 'label', 'id']
        read_only_fields = ('color',)

    def validate(self, data):
        orig_instance = self.instance
        new_instance = Transition(**data)
        if new_instance.is_approved and orig_instance.is_active is False:
            raise serializers.ValidationError('Can not approve a non active Transition')
        if new_instance.is_approved:
            orig_instance.is_active = False
            data['is_active'] = False
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['from'] = instance.start_block.id
        representation['to'] = instance.end_block.id
        representation.pop('start_block')
        representation.pop('end_block')
        if instance.start_block.is_conditional:
            representation['text'] = instance.label
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
        fields = ['history_id', 'history_date', 'history_user', 'label', 'is_active', 'is_approved']


class Custom2(serializers.Serializer):
    field = serializers.CharField(max_length=256, read_only=True)
    old = serializers.CharField(max_length=256, read_only=True)
    new = serializers.CharField(max_length=256, read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'label', 'text', 'last_modified','block', 'author']
        read_only_fields = ['last_modified']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        instance = Comment.objects.create(**validated_data)
        return instance
