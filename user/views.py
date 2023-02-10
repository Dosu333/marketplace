from django.conf import settings
from rest_framework.decorators import action
from rest_framework import filters, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import get_user_model, logout, login
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import viewsets, status, generics, views
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from .models import User
from .permissions import IsAdmin
from .serializers import (CreateUserSerializer, ListUserSerializer, AuthTokenSerializer, CustomObtainTokenPairSerializer,
                          InitializePasswordResetSerializer, CreatePasswordSerializer)


class AuthViewsets(viewsets.ModelViewSet):
    """User viewsets"""
    queryset = get_user_model().objects.all()
    serializer_class = ListUserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering_fields = ['created_at', 'last_login',
                       'email', 'first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == 'create_password':
            return CreatePasswordSerializer
        elif self.action == 'initialize_reset':
            return InitializePasswordResetSerializer
        elif self.action in ['create', 'invite_user']:
            return CreateUserSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ['create_password', 'initialize_reset', 'retrieve', 'list']:
            permission_classes = [AllowAny]
        elif self.action in ['destroy', 'partial_update']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(methods=['POST'], detail=False, serializer_class=CreateUserSerializer, permission_classes=[IsAuthenticated, IsAdmin], url_path='invite-user')
    def invite_user(self, request, pk=None):
        """This endpoint invites new user by admin"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True}, status=status.HTTP_200_OK)
            return Response({'success': False, 'errors': serializer.errors}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


    # @action(methods=['POST'], detail=False, serializer_class=InitializePasswordResetSerializer, url_path='reset-password')
    # def initialize_reset(self, request, pk=None):
    #     """This endpoint initializes password reset by sending password reset email to user"""
    #     try:
    #         serializer = self.get_serializer(data=request.data)
    #         if serializer.is_valid():
    #             email = request.data['email'].lower().strip()
    #             user = get_user_model().objects.filter(email=email, is_active=True).first()
    #             if not user:
    #                 return Response({'success': False, 'message': 'user with this record not found'}, status=status.HTTP_400_BAD_REQUEST)
    #             return Response({'success': True, 'message': 'Email successfully sent to registered email'}, status=status.HTTP_200_OK)
    #         return Response({'success': False, 'errors': serializer.errors}, status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(methods=['POST'], detail=False, serializer_class=CreatePasswordSerializer, url_path='create-password')
    # def create_password(self, request, pk=None):
    #     """Create a new password given the reset token"""
    #     try:
    #         serializer = self.get_serializer(data=request.data)
    #         if serializer.is_valid():
    #             token = Token.objects.filter(
    #                 token=request.data['token']).first()
    #             if not token or not token.is_valid():
    #                 return Response({'success': False, 'errors': 'Invalid token specified'}, status=status.HTTP_400_BAD_REQUEST)
    #             token.reset_user_password(request.data['password'])
    #             token.delete()
    #             return Response({'success': True, 'message': 'Password successfully reset'}, status=status.HTTP_200_OK)
    #         return Response({'success': False, 'errors': serializer.errors}, status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomObtainTokenPairView(TokenObtainPairView):
    """Login with email and password"""
    serializer_class = CustomObtainTokenPairSerializer


