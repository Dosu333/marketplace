from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailableInvestmentViewset

app_name = 'investment'

router = DefaultRouter()
router.register('investments', AvailableInvestmentViewset)

urlpatterns = [
    path('', include(router.urls))
]