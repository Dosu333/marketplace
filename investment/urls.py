from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailableInvestmentViewset, ActiveInvestmentViewSets

app_name = 'investment'

router = DefaultRouter()
router.register('investments', AvailableInvestmentViewset)
router.register('active-investments', ActiveInvestmentViewSets)

urlpatterns = [
    path('', include(router.urls))
]