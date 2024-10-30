from views import TransactionView, WalletView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('transactions', TransactionView)
router.register('wallets', WalletView)

