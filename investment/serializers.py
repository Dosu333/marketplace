from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

class AvailableInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableInvestment
        fields = ('__all__')

class CreateAvailableInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableInvestment
        exclude = ['investors', ]

class InvestorSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()

    def validate(self, attrs):
        user_id = attrs['user_id']
        if not get_user_model().objects.filter(id=str(user_id)):
            raise serializers.ValidationError('User does not exist')
        return attrs