from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
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

  
class ActiveInvestmentViewSets(viewsets.ModelViewSet):
    queryset = ActiveInvestment.objects.all()
    serializer_class = ActiveInvestmentSerializer
    http_method_names = ['get', ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset.filter(investor=self.request.user)
