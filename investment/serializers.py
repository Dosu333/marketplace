from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

class AvailableInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableInvestment
        fields = '__all__'

class CreateAvailableInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableInvestment
        fields = '__all__'

class ActiveInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveInvestment
        exclude = ['investor', 'reference']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = {'name': instance.product.name, 'amount': instance.product.amount, 'earnings': instance.product.earnings}
        return representation

class InvestorSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()

    def validate(self, attrs):
        user_id = attrs['user_id']
        if not get_user_model().objects.filter(id=str(user_id)):
            raise serializers.ValidationError('User does not exist')
        return attrs

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class InvestmentIDSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()

    def validate(self, attrs):
        if not AvailableInvestment.objects.filter(id=str(attrs['product_id'])):
            raise serializers.ValidationError('invalid product')
        return super().validate(attrs)
    
class WithdrawalSerializer(serializers.Serializer):
    receipient_account_number = serializers.CharField(max_length=10)
    receipient_bank = serializers.CharField(max_length=225, required=False)
    amount = serializers.IntegerField()