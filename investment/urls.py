from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailableInvestmentViewset, GetActiveInvestmentView, TransactionViewSet

app_name = 'investment'

router = DefaultRouter()
router.register('investments', AvailableInvestmentViewset)
router.register('transactions', TransactionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('active-investments/', GetActiveInvestmentView.as_view())
]