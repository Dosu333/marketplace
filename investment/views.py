from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from user.permissions import IsAdmin
from .models import AvailableInvestment
from .serializers import AvailableInvestmentSerializer, CreateAvailableInvestmentSerializer, InvestorSerializer

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
        elif self.action in ['list', 'add_investor', 'remove_investor']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated, ], url_path='add-investor')
    def add_investor(self, request, pk=None):
        """This endpoint adds user to an investment"""
        try:
            investment = self.get_object()
            user = get_user_model().objects.get(id=request.user.pk)
            investment.investors.add(user)
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False,'errors': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated, ], url_path='remove-investor')
    def remove_investor(self, request, pk=None):
        """This endpoint remove user from an investment"""
        try:
            investment = self.get_object()
            user = get_user_model().objects.get(id=request.user.pk)
            investment.investors.remove(user)
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False,'errors': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
