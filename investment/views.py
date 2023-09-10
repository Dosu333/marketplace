from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from user.permissions import IsAdmin
from .models import AvailableInvestment, ActiveInvestment, Transaction
from .serializers import (AvailableInvestmentSerializer, CreateAvailableInvestmentSerializer, InvestmentIDSerializer, 
                          ActiveInvestmentSerializer, TransactionSerializer, WithdrawalSerializer)
import requests

def paystack_verify(ref):
    url =  f'https://api.paystack.co/transaction/verify/{ref}'
    paystack_secret = 'sk_test_a911d08bd770ff828c18d123457a9b3e53853bc3'
    headers_dict = {'Authorization': "Bearer {}".format(paystack_secret)}
    r = requests.get(url, headers=headers_dict)
    response = r.json()
    if response['status']:
        if response['data']['status'] == 'success':
            return True
        return False
    return False
                         

class AvailableInvestmentViewset(viewsets.ModelViewSet):
    queryset = AvailableInvestment.objects.all()
    serializer_class = AvailableInvestmentSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateAvailableInvestmentSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class GetActiveInvestmentView(views.APIView):
    queryset = ActiveInvestment.objects.all()
    serializer_class = ActiveInvestmentSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            user_investments = self.queryset.filter(investor=request.user)
            results = user_investments.filter(cashed_out=False)
            serialized_results = self.serializer_class(results, many=True).data
            total_investments = user_investments.filter(
                investor=request.user).aggregate(Sum('product__amount'))
            total_profit = user_investments.filter(
                cashed_out=True).aggregate(Sum('product__amount'))
            return Response({"success": True, "total_investment": total_investments['product__amount__sum'], "total_profit": total_profit['product__amount__sum'], "results": serialized_results}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'sucess': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    http_method_names = ['get','post']
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'verify-transaction':
            return InvestmentIDSerializer
        elif self.action == 'withdraw':
            return WithdrawalSerializer
        return super().get_serializer_class()

    @action(methods=['POST'], detail=False,  url_path='verify-investment')
    def verify_investment(self, request, *args, **kwargs):
        ref = self.request.query_params.get('ref', None)
        serializer = InvestmentIDSerializer(data=request.data)

        try:
            if ref is not None and serializer.is_valid():
                if not paystack_verify(ref):
                    return Response({'success': False, 'errors':'something is wrong with paystack payment'}, status=status.HTTP_400_BAD_REQUEST)
                product = AvailableInvestment.objects.get(id=str(serializer.data['product_id']))
                ActiveInvestment.objects.create(product=product, investor=request.user, reference=ref)
                self.queryset.create(reference=ref,transaction_type='DEPOSIT')
                return Response({'success': True}, status=status.HTTP_200_OK)
            return Response({'success': False, 'errors':'invalid reference or product id'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success':False,'errors': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(methods=['POST'], detail=False,  url_path='withdraw')
    def withdraw(self, request, *args, **kwargs):
        serializer = WithdrawalSerializer(data=request.data)
        try:
            if serializer.is_valid():
                data = serializer.data
                if request.user.profit_balance < data['amount']:
                    return Response({'success': False, 'error': 'insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
                # paystack transfer
        except Exception as e:
            return Response({'success':False,'errors': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'success': False, 'error': serializer.error}, status=status.HTTP_400_BAD_REQUEST)
