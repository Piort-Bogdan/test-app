from django.urls import path

from app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transactions', views.TransactionViewSet, basename='transaction')
router.register(r'wallets', views.WalletViewSet, basename='wallet')
