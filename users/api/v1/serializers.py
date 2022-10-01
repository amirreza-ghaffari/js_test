from rest_framework import serializers
from users.models import CustomUser, Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
