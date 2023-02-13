from rest_framework import serializers
from .models import *

class AvailableInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableInvestment
        fields = ('__all__')