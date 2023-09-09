from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from user.permissions import IsAdmin
from .models import AvailableInvestment, ActiveInvestment
from .serializers import AvailableInvestmentSerializer, CreateAvailableInvestmentSerializer, InvestorSerializer, ActiveInvestmentSerializer


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
